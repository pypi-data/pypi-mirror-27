import pytest
from django.conf import settings
from django.core.management import call_command
from organizations.models import Organization


@pytest.fixture()
def seed_data():
    call_command('seed', nb_organizations=2, nb_contacts=20, nb_contacts_groups=6, nb_campaigns=6)


@pytest.fixture(scope='session')
def celery_eager_mode():
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture()
def create_test_organization():
    return Organization.objects.create(name='Test Org')
