# coding: utf-8
from django.utils.deprecation import MiddlewareMixin

from djotali.billing.models import Credit


class CreditMiddleware(MiddlewareMixin):
    """
    Will set the organization credit in request so that it can be displayed in views.
    Should be declared after djotali.profile.middleware.OrganizationMiddleware as it requires info processed there.
    """

    def process_request(self, request):
        if not hasattr(request, "organization"):
            return
        organization = request.organization
        request.credit = Credit.get_credit_amount(organization) if organization else None
