# coding: utf-8
from django.forms.fields import CharField

from djotali.contacts.models import Contact


class CsvContact:
    first_name = CharField()
    last_name = CharField()
    phone_number = CharField()

    def to_model(self):
        """
        Transform plain CsvContact object to Contact Django Model
        """
        c = Contact()
        c.first_name = self.first_name
        c.last_name = self.last_name
        c.phone_number = self.phone_number
        c.organization_id = 1  # TODO: Get organization
        return c

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.phone_number)
