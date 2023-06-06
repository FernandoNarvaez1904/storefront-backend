from django.db import models
from django.db.models import OneToOneRel
from django.db.models.signals import pre_save
from django.dispatch import receiver
from strawberry_django_plus import gql

from documents.models import Document
from inventory.models import Item


class StockMovementAction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="stock_movements")
    parent_document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name="stock_movements")
    modification_amount = models.FloatField()
    description = models.TextField(null=True, blank=True)
    is_cumulative = models.BooleanField(default=True)

    item_cost = models.FloatField(blank=True)
    item_markup = models.FloatField(blank=True)
    item_price = models.FloatField(blank=True)
    modification_cost_value = models.FloatField(blank=True)
    modification_price_value = models.FloatField(blank=True)
    creation_date = models.DateTimeField(blank=True)

    @gql.model_cached_property(select_related=["parent_document"])
    async def document_type(self):
        doc: OneToOneRel = self.parent_document._meta.related_objects[1]
        return doc.related_model.__name__


@receiver(pre_save, sender=StockMovementAction)
def populate_fields_from_item(sender, instance: StockMovementAction, *args, **kwargs):
    instance.item_cost = instance.item.cost
    instance.item_markup = instance.item.markup
    instance.item_price = instance.item.price_c
    instance.modification_cost_value = instance.item_cost * instance.modification_amount
    instance.modification_price_value = instance.item_price * instance.modification_amount
    instance.creation_date = instance.parent_document.creation_date
