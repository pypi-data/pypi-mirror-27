from uuid import uuid4

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import F
from django_prices.models import PriceField
from prices import Price
from satchless.item import Item, ItemLine

from djotali.billing.exceptions import NotEnoughCredit
from djotali.campaigns.models import Campaign
from djotali.core.models import TrackedModel
from djotali.profile.models import AbstractOrganizationAsset


class Credit(TrackedModel, AbstractOrganizationAsset):
    credit = models.IntegerField()

    @staticmethod
    def get_credit_amount(organization):
        return Credit.objects.get(organization=organization).credit

    class Meta:
        unique_together = ('organization',)


class CampaignAllocatedCredit(TrackedModel, AbstractOrganizationAsset):
    allocated_credit = models.IntegerField()
    campaign = models.OneToOneField(Campaign, )

    @staticmethod
    def allocate(campaign, credit_to_allocate):
        organization = campaign.organization
        organization_credit = Credit.objects.get(organization=organization).credit
        if organization_credit < credit_to_allocate:
            raise NotEnoughCredit
        Credit.objects.filter(organization=organization).update(credit=organization_credit - credit_to_allocate)
        campaign_allocated_credit = CampaignAllocatedCredit.all.update_or_create(campaign=campaign, defaults={
            'allocated_credit': credit_to_allocate,
            'organization': campaign.organization,
            'is_removed': False
        })
        return campaign_allocated_credit

    @staticmethod
    def consume_one(campaign_id):
        with transaction.atomic():
            allocated_credit = CampaignAllocatedCredit.objects.get(campaign_id=campaign_id)
            allocated_credit.allocated_credit -= 1
            allocated_credit.save()
            if allocated_credit.allocated_credit < 1:
                allocated_credit.delete()
            return allocated_credit

    @staticmethod
    def deallocate_one(campaign_id):
        with transaction.atomic():
            if not CampaignAllocatedCredit.objects.filter(campaign_id=campaign_id).first():
                return
            allocated_credit = CampaignAllocatedCredit.consume_one(campaign_id)
            CampaignAllocatedCredit._add_to_credit(allocated_credit.organization, 1)

    @staticmethod
    def deallocate_and_credit(campaign_id):
        with transaction.atomic():
            allocated_credit = CampaignAllocatedCredit.objects.filter(campaign_id=campaign_id).first()
            if not allocated_credit:
                # In this case it has probably been de-allocated by consume_one if no allocated credit was left
                return
            CampaignAllocatedCredit._add_to_credit(allocated_credit.organization, allocated_credit.allocated_credit)
            allocated_credit.delete()

    @staticmethod
    def _add_to_credit(organization, amount):
        Credit.objects.filter(organization=organization).update(credit=F('credit') + amount)


class ProductManager(models.Manager):
    def get_published_products(self):
        return self.get_queryset().filter(is_published=True)


class Product(TrackedModel, Item):
    name = models.CharField(max_length=100, blank=True, unique=True)
    description = models.TextField()
    price = PriceField(currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2)
    is_published = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def get_price_per_item(self, **kwargs):
        return self.price

    def description_lines(self):
        return self.description.split('\n')

    def formatted_net_price(self):
        # TODO change when there will be i18n
        return '{:,}'.format(self.price.net).rstrip('0').rstrip('.').replace(',', '.')


class Cart(TrackedModel, AbstractOrganizationAsset):
    """A shopping cart."""
    token = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    total = PriceField(currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2, default=0)

    # pylint: disable=R0201
    def get_subtotal(self, item, **kwargs):
        """Return the cost of a cart line."""
        return item.get_total(**kwargs)

    def get_total(self, **kwargs):
        """Return the total cost of the cart prior to shipping."""
        subtotals = [
            self.get_subtotal(item, **kwargs) for item in self.lines.all()]
        if not subtotals:
            raise AttributeError('Calling get_total() on an empty item set')
        zero = Price(0, currency=settings.DEFAULT_CURRENCY)
        return sum(subtotals, zero)

    def count(self):
        """Return the total quantity in cart."""
        lines = self.lines.all()
        return lines.aggregate(total_quantity=models.Sum('quantity'))

    def clear(self):
        """Remove the cart."""
        self.delete()

    def create_line(self, product, quantity):
        """Create a cart line for given variant, quantity and optional data.
        The `data` parameter may be used to differentiate between items with
        different customization options.
        """
        return self.lines.create(product=product, quantity=quantity)

    def get_line(self, product):
        """Return a line matching the given variant and data if any."""
        all_lines = self.lines.all()
        line = [line for line in all_lines if line.variant_id == product.id]
        if line:
            return line[0]

    def add(self, variant, quantity=1, replace=False):
        """Add a product to cart.
        The `data` parameter may be used to differentiate between items with
        different customization options.
        If `replace` is truthy then any previous quantity is discarded instead
        of added to.
        """
        cart_line, dummy_created = self.lines.get_or_create(variant=variant, defaults={'quantity': 0})

        if replace:
            new_quantity = quantity
        else:
            new_quantity = cart_line.quantity + quantity

        if new_quantity < 0:
            raise ValueError('%r is not a valid quantity (results in %r)' % (quantity, new_quantity))

        cart_line.quantity = new_quantity

        if not cart_line.quantity:
            cart_line.delete()
        else:
            cart_line.save(update_fields=['quantity'])


class CartLine(TrackedModel, ItemLine):
    """A single cart line.
    Multiple lines in the same cart can refer to the same product variant if
    their `data` field is different.
    """

    cart = models.ForeignKey(Cart, related_name='lines', on_delete=models.CASCADE)
    product = models.ForeignKey('billing.Product', related_name='+', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])

    class Meta:
        unique_together = ('cart', 'product',)

    def __eq__(self, other):
        if not isinstance(other, CartLine):
            return NotImplemented

        return self.product == other.product and self.quantity == other.quantity

    def __ne__(self, other):
        return not self == other  # pragma: no cover

    def __repr__(self):
        return 'CartLine(product=%r, quantity=%r)' % (self.product, self.quantity)

    def __getstate__(self):
        return self.product, self.quantity

    def __setstate__(self, data):
        self.product, self.quantity = data

    def get_quantity(self, **kwargs):
        """Return the line's quantity."""
        return self.quantity

    # pylint: disable=W0221
    def get_price_per_item(self, discounts=None, **kwargs):
        """Return the unit price of the line."""
        return self.product.get_price_per_item(discounts=discounts, **kwargs)
