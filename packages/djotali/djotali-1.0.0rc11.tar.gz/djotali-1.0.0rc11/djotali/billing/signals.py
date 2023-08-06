from djotali.billing.models import Credit


def create_credit_line_on_organization_creation(sender, instance, created, **kwargs):
    if created:
        Credit.objects.create(organization=instance, credit=0)
