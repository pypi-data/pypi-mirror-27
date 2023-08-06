# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views import generic

from djotali.billing.models import Credit, CampaignAllocatedCredit, Product


# TODO becomes a generic.ListView when we will introduce transactions
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'billing/show.html'
    queryset = Product.objects.get_published_products
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['credit'] = Credit.objects.get(organization=self.request.organization)
        allocated_credit = \
            CampaignAllocatedCredit.objects.filter(organization=self.request.organization).aggregate(Sum('allocated_credit'))['allocated_credit__sum']
        data['allocated_credit'] = allocated_credit if allocated_credit else 0
        return data
