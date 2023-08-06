import os

import tldextract
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import BaseCommand


class Command(BaseCommand):
    _admin_username = 'admin@mg.djotali.com'
    help = 'Bootstrap application'

    def handle(self, *args, **options):
        # Create the admin user for the platform
        # We get a default password only in dev environment, on other environment if pwd is not provided as env var, it will raise an exception
        pwd = os.getenv('ADMIN_PWD', 'changeme') if os.getenv('DEV') else os.getenv('ADMIN_PWD')
        self.stdout.write(self.style.WARNING('Bootstrapping the app...'))

        self.stdout.write(self.style.WARNING('Setting up the admin...'))
        if pwd is None:
            return
        if User.objects.filter(username=self._admin_username).exists():
            User.objects.get(username=self._admin_username).set_password(pwd)
        else:
            User.objects.create_superuser(self._admin_username, self._admin_username, pwd)

        self.stdout.write(self.style.WARNING('Setting up django site...'))
        extracted_site_name = tldextract.extract(settings.SITE_NAME)
        site_domain = "{}.{}".format(extracted_site_name.domain, extracted_site_name.suffix)
        Site.objects.update_or_create(id=1, defaults={'name': settings.SITE_NAME, 'domain': site_domain})

        self.stdout.write(self.style.SUCCESS('Bootstrap done.'))


if __name__ == '__main__':
    extract_result = tldextract.extract('test-app.djotali.com')
    "{}.{}".format(extract_result.domain, extract_result.suffix)
