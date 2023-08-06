# Create your models here.
from django.db import models
from model_utils.managers import SoftDeletableManager
from organizations.models import Organization
from rest_framework import serializers

from djotali.core.models import TrackedModel


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name',)


class OrganizationAssetManager(SoftDeletableManager):
    def get_queryset_for_organization(self, organization):
        return super(OrganizationAssetManager, self).get_queryset().filter(organization__id=organization.id)


class AbstractOrganizationAsset(models.Model):
    organization = models.ForeignKey(Organization)

    org_objects = OrganizationAssetManager()

    class Meta:
        abstract = True


class Sender(TrackedModel, AbstractOrganizationAsset):
    sender_id = models.CharField(max_length=11, blank=False, null=False)
