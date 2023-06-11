from django.db import models
from strawberry_django_plus import gql

from documents.models import Document
from inventory.models import Item


class StockMovementAction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="stock_movements")
    parent_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="stock_movements")
    modification_amount = models.FloatField()
    description = models.TextField(null=True, blank=True)
    is_cumulative = models.BooleanField(default=True)

    item_cost = models.FloatField(blank=True)
    item_markup = models.FloatField(blank=True)
    item_price = models.FloatField(blank=True)
    modification_cost_value = models.FloatField(blank=True)
    modification_price_value = models.FloatField(blank=True)
    creation_date = models.DateTimeField(blank=True)

    @gql.model_cached_property
    async def document_type(self):
        return self.parent_document._meta.object_name
