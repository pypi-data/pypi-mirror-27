# coding: utf-8

from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives

from djotali.celery import app as celery_app

logger = get_task_logger(__name__)


@celery_app.task
def send_email(subject, body, from_email, to_emails):
    logger.debug('Mail with subject {} has been sent to {}'.format(subject, to_emails))
    email = EmailMultiAlternatives(subject, subject, from_email, to_emails)
    print(body)
    email.attach_alternative(body, "text/html")
    email.send()
