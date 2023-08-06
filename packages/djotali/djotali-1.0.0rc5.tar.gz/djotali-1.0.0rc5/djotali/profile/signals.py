import re

from django.contrib.auth.models import User
from django.template import loader
from django.urls import reverse
from organizations.models import OrganizationOwner, Organization

from djotali.core.utils import get_logger
from djotali.profile.models import Sender

_subject_template = 'profile/new_signup_email_subject.txt'
_body_template = 'profile/new_signup_email_body.html'

_logger = get_logger(__name__)


def create_sender(request, user, **kwargs):
    sender_id = request.POST['sender_id']
    organization_name = request.POST['organization']
    organization = Organization.objects.get(name=organization_name)
    if not re.match('^[a-zA-Z]{0,11}$', sender_id):
        # TODO not enough time but should be rejected before creating user and organization in the appropriate view
        # But this is sufficient to forbid sms sending at the moment
        _logger.warning('This sign up request is not from our application. Sender ID {} will not be created'.format(sender_id))
        return
    Sender.objects.create(organization=organization, sender_id=sender_id[:11])


def alert_admin(request, user, **kwargs):
    # Important to import locally or it won't be possible to mock
    from djotali.core.tasks.jobs import send_email
    organization_name = request.POST['organization']
    owner = OrganizationOwner.objects.get(organization__name__iexact=organization_name)
    organization_owner_user = User.objects.get(
        organizations_organizationuser__id=owner.organization_user.id,
    )
    # Username is the user's email in our current flow
    owner_email = organization_owner_user.username

    subject_template = loader.get_template(_subject_template)
    subject = subject_template.render({
        'organization': organization_name,
    })

    body_template = loader.get_template(_body_template)
    body = body_template.render({
        # Username is the user's email in our current flow
        'signup_email': user.username,
        'organization': organization_name,
        'activate_url': reverse('profile:activate-users'),
    })

    send_email.delay(
        subject,
        body,
        'donotreply@mg.djotali.com',
        [owner_email],
    )
