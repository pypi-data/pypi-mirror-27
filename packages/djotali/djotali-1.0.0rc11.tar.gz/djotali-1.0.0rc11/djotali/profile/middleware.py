# coding: utf-8
from django.utils.deprecation import MiddlewareMixin
from organizations.models import Organization


class OrganizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if not user or not user.id or user.is_staff:
            return
        organization = request.session.get('organization')
        is_organization_admin = request.session.get('is_organization_admin')
        if organization is None or is_organization_admin:
            # A user has one and only one organization that is created on signup
            organization = Organization.active.filter(users__id=user.id)[0]
            is_organization_admin = organization.is_admin(user)
        request.session['organization'] = organization
        request.session['is_organization_admin'] = is_organization_admin
        request.organization = organization
        request.is_organization_admin = is_organization_admin
