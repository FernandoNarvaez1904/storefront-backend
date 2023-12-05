from django.db import models
import strawberry_django

from documents.models import Document
from inventory.models import Item


class StockMovementAction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="stock_movements")
    parent_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="stock_movements")
    modification_amount = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.TextField(null=True, blank=True)

    is_cumulative = models.BooleanField(default=True)

    item_cost = models.DecimalField(decimal_places=2, blank=True, max_digits=12)
    item_markup = models.DecimalField(decimal_places=2, blank=True, max_digits=12)
    item_price = models.DecimalField(decimal_places=2, blank=True, max_digits=12)
    creation_date = models.DateTimeField(blank=True)

    @strawberry_django.django_resolver
    async def document_type(self):
        return self.parent_document._meta.object_name
