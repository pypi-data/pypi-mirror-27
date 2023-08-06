import logging

from django.apps import AppConfig
from django.conf import settings
from django.utils.functional import cached_property

from djotali.core.services import ConsoleSmsSender, MessageBirdSmsSender

_logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    name = 'djotali.core'
    verbose_name = 'core'

    @cached_property
    def sms_sender(self):
        if settings.MESSAGEBIRD_TOKEN:
            return MessageBirdSmsSender(settings.MESSAGEBIRD_TOKEN)
        return ConsoleSmsSender(settings.CONSOLE_SMS_MAX_TIMEOUT, settings.CONSOLE_SMS_MIN_TIMEOUT)
