# coding: utf-8

from allauth.account.models import EmailAddress, EmailConfirmation
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from organizations.models import Organization
from prices import Price

from djotali.billing.models import Product
from djotali.campaigns.models import Campaign, Notification
from djotali.contacts.models import Contact, ContactsGroup
from djotali.core.seed.factories import ContactsGroupFactory, CampaignFactory, OrganizationFactory, ContactFactory


class Command(BaseCommand):
    help = 'Seed Database'

    def add_arguments(self, parser):
        # Optional arguments
        parser.add_argument(
            '--nb-organizations',
            default=3,
            dest='nb_organizations',
            help='The number of organizations to create',
        )
        parser.add_argument(
            '--nb-contacts',
            default=250,
            dest='nb_contacts',
            help='The number of contacts to create',
        )
        parser.add_argument(
            '--nb-contacts-groups',
            default=12,
            dest='nb_contacts_groups',
            help='The number of contacts groups to create',
        )
        parser.add_argument(
            '--nb-campaigns',
            default=15,
            dest='nb_campaigns',
            help='The number of campaigns to create',
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            try:
                nb_organizations = options['nb_organizations']
                nb_contacts = options['nb_contacts']
                nb_contacts_groups = options['nb_contacts_groups']
                nb_campaigns = options['nb_campaigns']

                # Drop all application data first
                self.stdout.write(self.style.WARNING('Truncating tables first...'))
                Organization.objects.all().delete()
                User.objects.all().delete()
                EmailAddress.objects.all().delete()
                EmailConfirmation.objects.all().delete()
                ContactsGroup.objects.all().delete()
                Contact.objects.all().delete()
                Campaign.objects.all().delete()
                Notification.objects.all().delete()

                OrganizationFactory.create_batch(nb_organizations)

                contacts = ContactFactory.create_batch(nb_contacts)
                ContactsGroupFactory.create_batch(nb_contacts_groups, contacts=contacts)
                CampaignFactory.create_batch(nb_campaigns)

                Product.objects.update_or_create(name='Pack économique',
                                                 defaults={
                                                     'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\nAenean commodo ligula eget '
                                                                    'dolor. Aenean massa.',
                                                     'price': Price(5000, currency='XOF')
                                                 })

                Product.objects.update_or_create(name='Pack premium',
                                                 defaults={
                                                     'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\nAenean commodo ligula eget '
                                                                    'dolor. Aenean massa.',
                                                     'price': Price(10000, currency='XOF')
                                                 })

                Product.objects.update_or_create(name='Pack business',
                                                 defaults={
                                                     'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\nAenean commodo ligula eget '
                                                                    'dolor. Aenean massa.',
                                                     'price': Price(15000, currency='XOF')
                                                 })

                Product.objects.update_or_create(name='Pack not published',
                                                 defaults={
                                                     'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\nAenean commodo ligula eget '
                                                                    'dolor. Aenean massa.',
                                                     'price': Price(20000, currency='XOF'),
                                                     'is_published': False
                                                 })

                call_command('bootstrap')
                self.stdout.write(self.style.SUCCESS('Database seeded'))
            except CommandError as e:
                self.stdout.write(self.style.ERROR('Failed to seed database. Rolling back transaction', e))
