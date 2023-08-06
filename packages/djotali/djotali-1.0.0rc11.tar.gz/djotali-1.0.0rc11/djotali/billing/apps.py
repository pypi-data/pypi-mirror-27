# coding: utf-8

from django.apps import AppConfig
from django.db.models.signals import post_save


class BillingConfig(AppConfig):
    name = 'djotali.billing'

    def ready(self):
        from djotali.billing.signals import create_credit_line_on_organization_creation
        post_save.connect(create_credit_line_on_organization_creation, sender='organizations.Organization')
