# coding: utf-8
import errno
import os

import unicodecsv as csv
from django.conf import settings
from django.core.files.storage import default_storage
from faker.factory import Factory

from djotali.contacts.csv.models import CsvContact
from djotali.contacts.models import Contact
from djotali.contacts.templatetags.contacts_extras import format_number
from djotali.core.seed import SenegalesePhoneNumberProvider


class CsvUtil:
    def __init__(self, delimiter=";"):
        self.delimiter = delimiter

    def create_csv_model(self, headers=None):
        path = settings.MEDIA_ROOT + '/model.csv'

        if default_storage.exists(path):
            return path

        if headers is None:
            headers = ['Nom', 'Prenom', 'Telephone']

        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(path, 'w+b') as file_path:
            writer = csv.writer(file_path, delimiter=self.delimiter, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
            faker = Factory.create('fr_FR')
            faker.add_provider(SenegalesePhoneNumberProvider)
            phone_number = format_number(faker.senegal_phone_number())
            writer.writerow([
                faker.first_name(),
                faker.last_name(),
                phone_number,
            ])
        return path

    @staticmethod
    def _format(row):
        return [
            column.encode('utf-8').decode('utf-8')
            for column in row
        ]

    def import_csv(self, csv_file):
        # Process into Celery Task ?
        reader = csv.reader(csv_file, delimiter=self.delimiter)
        next(reader)
        contacts = []
        for row in reader:
            c = CsvContact()
            c.last_name = row[0]
            c.first_name = row[1]
            c.phone_number = row[2]
            contacts.append(c.to_model())
        if len(contacts) > 0:
            Contact.objects.bulk_create(contacts, batch_size=20)
        else:
            raise ValueError('No Data into CSV File')
