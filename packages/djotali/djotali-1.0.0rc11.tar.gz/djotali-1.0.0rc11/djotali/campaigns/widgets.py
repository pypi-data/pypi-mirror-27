# coding: utf-8
from django import forms
from django.conf import settings
from django.urls import reverse

from djotali.core.widgets import BoundModelsSelectWidget, CoreWidget


class CampaignContactsGroupBoundModelsSelectWidget(BoundModelsSelectWidget):
    def get_url(self, value):
        if value is None:
            return None
        return reverse('contacts-groups:edit', args=(value,))

    def get_label(self):
        return 'Editer le groupe de contacts actuel'


class SmsWidget(forms.widgets.Input, CoreWidget):
    template_name = 'campaigns/widgets/sms-text.html'

    class Media:
        js = (
            settings.VUE_LIB,
            settings.VUEX_LIB,
            'js/sms-counter.min.js',
            'js/sms-text.component.js',
        )
