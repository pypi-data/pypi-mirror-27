# coding: utf-8
import datetime

import celery
import pytz
from billiard.exceptions import SoftTimeLimitExceeded
from celery import chord
from celery.exceptions import Reject
from celery.utils.log import get_task_logger
from django.apps import apps
from django.shortcuts import get_object_or_404

from djotali.billing.models import CampaignAllocatedCredit
from djotali.campaigns.models import Campaign, Notification
from djotali.celery import app as celery_app
from djotali.contacts.templatetags.contacts_extras import format_number
from djotali.core.utils import is_celery_running
from djotali.profile.models import Sender

logger = get_task_logger(__name__)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Check campaign to be launched every hour
    # This mechanism is set up to avoid putting campaigns in the queue for days even months
    # Their launch will be set up in the hour before their effective start date
    sender.add_periodic_task(
        3600.,
        set_up_campaigns_that_should_be_launched_in_the_next_hour.s(),
    )


@celery_app.task(max_retries=2, default_retry_delay=5)
def set_up_campaigns_that_should_be_launched_in_the_next_hour():
    broker_running = is_celery_running()
    if broker_running:
        return

    pristine_campaigns = Campaign.get_pristine_campaigns_from_today_s_midnight_to_the_next_hour_from_now_query()
    for pristine_campaign in pristine_campaigns.all():
        start_date = pristine_campaign.start_date
        countdown = 0
        utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        if start_date >= utc_now:
            countdown = (start_date - utc_now).total_seconds()
        notify_campaign.delay(pristine_campaign.id, countdown=countdown)


class NotifyLogger:
    def __init__(self, campaign_id, campaign_name, phone_number):
        self.pattern = 'CAMP_ID({}) - CAMP_NAME({}) - PHONE_NB({}) '.format(campaign_id, campaign_name, phone_number)

    def debug(self, message):
        logger.debug(self.pattern + message)

    def info(self, message):
        logger.info(self.pattern + message)

    def warning(self, message):
        logger.warning(self.pattern + message)

    def error(self, message):
        logger.error(self.pattern + message)


@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def notify_campaign(self, campaign_id):
    try:
        _launch_campaign(campaign_id)
    except Campaign.DoesNotExist as e:
        logger.error('Unable to find Campaign %s' % campaign_id)
        raise Reject(e, requeue=False)
    except RuntimeError as e:
        logger.warning('Campaign {} failed because of {}'.format(campaign_id, e))
        raise self.retry(exc=e, countdown=5)


class Notify(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info('The phone number {} has been successfully notified'.format(args[1]))
        Notify._tag_and_deallocate(args, Notification.tag_as_sent, CampaignAllocatedCredit.consume_one)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('Notification definitely failed for {}'.format(args[1]))
        Notify._tag_and_deallocate(args, Notification.tag_as_failed, CampaignAllocatedCredit.deallocate_one)

    @staticmethod
    def _tag_and_deallocate(args, tag_fn, credit_usage_fn):
        notification_id = args[0]
        tag_fn(notification_id)
        campaign_id = args[4]
        credit_usage_fn(campaign_id)


@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def notify_task(campaign_id, notification_id):
    _launch_campaign(campaign_id, notification_id)


@celery_app.task(base=Notify, bind=True, max_retries=2, soft_time_limit=5, throws=SoftTimeLimitExceeded)
def notify(self, notification_id, contact_phone_number, campaign_message, campaign_name, campaign_id):
    Notification.tag_as_in_progress(notification_id)
    # Create credit allocated to campaign if it does not exist yet
    allocated_credit = CampaignAllocatedCredit.objects.filter(campaign_id=campaign_id).first()
    if not allocated_credit:
        campaign = Campaign.objects.get(id=campaign_id)
        organization = campaign.organization
        CampaignAllocatedCredit.allocate(campaign, 1)
    else:
        organization = allocated_credit.organization

    contact_phone_number = format_number(contact_phone_number)
    notify_logger = NotifyLogger(campaign_id, campaign_name, contact_phone_number)
    try:
        notify_logger.debug('Sending notification')
        sent = apps.get_app_config('core').sms_sender.send(Sender.objects.get(organization=organization).sender_id, contact_phone_number, campaign_message)
        if not sent:
            notify_logger.error('An error occurs while sending message ! Retrying...')
            raise self.retry(countdown=60)
        return sent
    except Notification.DoesNotExist as e:
        notify_logger.error('Unable to find Notification %s' % notification_id)
        raise Reject(reason=e, requeue=False)
    except SoftTimeLimitExceeded as e:
        notify_logger.warning('Request timeout for notification - Retrying')
        raise self.retry(exc=e, countdown=5)
    except RuntimeError as e:
        raise self.retry(exc=e, countdown=2)


# TODO one method for campaign, one for single notif
def _launch_campaign(campaign_id, notification_id=None):
    if is_campaign_launched(campaign_id):
        return

    campaign = get_object_or_404(Campaign, pk=campaign_id)
    if not campaign.is_started():
        logger.warning('Campaign %s (%s) not started !' % (campaign.name, campaign.id))
        raise Reject(None, requeue=False)

    # TODO refactor this part by giving a function that filter the query appropriately
    notifications_query = Notification.objects
    if not notification_id:
        notifications_query = notifications_query.filter(campaign_id=campaign_id)
    else:
        notifications_query = notifications_query.filter(id=notification_id)

    notifications = notifications_query.exclude(status=1)

    nb_notifications = len(notifications)
    if nb_notifications == 0:
        logger.info('No notification to send for campaign {} ({}) and notification id {}'.format(campaign.name, campaign_id, notification_id))
        return

    # We allocate credit for the campaign
    CampaignAllocatedCredit.allocate(campaign=campaign, credit_to_allocate=nb_notifications)

    # Launch the notifications and reallocate unused credit afterwards
    campaign_notification_tasks = \
        [notify.subtask(args=(notif.id, notif.contact.phone_number, campaign.message, campaign.name, campaign.id)) for notif in notifications]

    chord(campaign_notification_tasks)(deallocate_unused_credit.s(campaign_id))


@celery_app.task
def deallocate_unused_credit(campaign_notification_results, campaign_id):
    CampaignAllocatedCredit.deallocate_and_credit(campaign_id)


def is_campaign_launched(campaign_id):
    return CampaignAllocatedCredit.objects.filter(campaign_id=campaign_id).exists()
