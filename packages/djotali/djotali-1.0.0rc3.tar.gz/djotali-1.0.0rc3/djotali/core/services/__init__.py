# coding: utf-8
import random
from time import sleep

import messagebird

from djotali.core.utils import get_logger

logger = get_logger(__name__)


class SmsSender:
    def send(self, organization_name, number, message):
        raise NotImplementedError


class ConsoleSmsSender(SmsSender):
    def __init__(self, max_timeout, min_timeout):
        self.max_timeout = max_timeout
        self.min_timeout = min_timeout

    def send(self, organization_name, number, message):
        try:
            logger.info('Sending {} to {}'.format(message, number))
            delay = ConsoleSmsSender.delay(self.min_timeout, self.max_timeout)
            logger.info('Task is going to take {}s'.format(delay))
            sleep(delay)
            logger.info('Message successfully sent.')
            return True
        except RuntimeError as e:
            logger.error(e)
        # It's better to raise an Error and Catch it Outside
        return False

    @staticmethod
    def delay(min_timeout, max_timeout):
        factor = 1
        while min_timeout * factor < 1:
            factor *= 10
        return random.choice(range(int(min_timeout * factor), int(max_timeout * factor))) / factor


class MessageBirdSmsSender(SmsSender):
    def __init__(self, messagebird_token):
        self.client = messagebird.Client(messagebird_token)

    def send(self, organization_name, number, message):
        try:
            # TODO Use the sms sending status
            self.client.message_create(
                originator=organization_name,
                recipients=[number],
                body=message
            )
            return True
        except messagebird.client.ErrorException as e:
            errors = [
                'MessageBird error trying to send sms for organization {} {} {} {}'.format(organization_name, error.code, error.description, error.parameter)
                for error in e.errors
            ]
            for error in errors:
                logger.error(error)
