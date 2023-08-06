# coding: utf-8

from django import forms

from djotali.campaigns.models import Campaign
from djotali.campaigns.widgets import CampaignContactsGroupBoundModelsSelectWidget, SmsWidget
from djotali.contacts.models import ContactsGroup
from djotali.core.forms import BaseForm
from djotali.core.widgets import DateTimeFieldWidget


class CampaignForm(BaseForm):
    class Meta:
        model = Campaign
        fields = ['name', 'start_date', 'message', 'contacts_group']

    name = forms.CharField(label='Nom')
    start_date = forms.DateTimeField(label='Lancement', widget=DateTimeFieldWidget)
    message = forms.Field(label='Message', widget=SmsWidget)
    contacts_group = forms.ModelChoiceField(label='Groupe de contacts', queryset=ContactsGroup.objects,
                                            widget=CampaignContactsGroupBoundModelsSelectWidget,
                                            empty_label='Tous les contacts', required=False)

    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        self.fields['contacts_group'].queryset = ContactsGroup.org_objects.get_queryset_for_organization(self.request.organization)
