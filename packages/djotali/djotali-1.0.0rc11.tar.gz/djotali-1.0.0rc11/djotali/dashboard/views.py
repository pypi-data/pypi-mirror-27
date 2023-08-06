# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from djotali.billing.models import Credit
from djotali.campaigns.models import Campaign, Notification
from djotali.contacts.models import Contact


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if hasattr(self.request, 'organization'):
            organization = self.request.organization
            context['total_credit'] = Credit.org_objects.get_queryset_for_organization(organization).first().credit
            context['total_contacts'] = Contact.org_objects.get_queryset_for_organization(organization).count()
            context['sent_messages'] = Notification.org_objects.get_queryset_for_organization(organization).filter(status=1).count()
            context['failed_messages'] = Notification.org_objects.get_queryset_for_organization(organization).filter(status=-1).count()
            context['next_campaigns'] = Campaign.get_closest_campaigns_query_set().filter(organization=organization)[:5]
        return context
