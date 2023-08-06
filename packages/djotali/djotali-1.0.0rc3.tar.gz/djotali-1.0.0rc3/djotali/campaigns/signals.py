from djotali.campaigns.models import Campaign, Notification
from djotali.contacts.models import ContactsGroup


def update_notifications_after_contact_save(sender, instance, created, **kwargs):
    organization = instance.organization
    if created:
        # We create the appropriate notification when a contact is created on campaigns linked to all contacts group
        campaigns_linked_to_all_groups = Campaign.get_linked_to_all_contacts_group(organization)
        notifications = []
        for campaign in campaigns_linked_to_all_groups:
            notifications.append(Notification(contact=instance, campaign=campaign, organization=organization, status=None))
        Notification.objects.bulk_create(notifications)


def update_notifications_after_campaign_save(sender, instance, created, **kwargs):
    organization = instance.organization
    if not created and Notification.objects.filter(campaign=instance, contacts_group=instance.contacts_group).exists():
        return
    elif not created:
        Notification.objects.filter(campaign=instance).delete()

    # We create notifications associated to contacts
    notifications = []
    for contact in ContactsGroup.get_contacts_queryset(instance.contacts_group, organization).all():
        notifications.append(Notification(contact=contact, contacts_group=instance.contacts_group, campaign=instance, status=None, organization=organization))
    Notification.objects.bulk_create(notifications)
