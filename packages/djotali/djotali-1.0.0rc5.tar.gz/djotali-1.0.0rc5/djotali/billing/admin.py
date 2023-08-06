# coding: utf-8

from django.contrib import admin

from djotali.billing import models


class CreditAdmin(admin.ModelAdmin):
    model = models.Credit
    list_display = ('organization', 'credit')


class CampaignAllocatedCreditAdmin(admin.ModelAdmin):
    model = models.CampaignAllocatedCredit
    list_display = ('organization', 'campaign', 'allocated_credit')


admin.site.register(models.Credit, CreditAdmin)
admin.site.register(models.CampaignAllocatedCredit, CampaignAllocatedCreditAdmin)
