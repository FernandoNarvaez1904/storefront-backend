from django.db import models

from document_management.models import DocumentInterface
from inventory.models.item_model import Item


class ModifyStockOrder(DocumentInterface):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="stock_changes")
    quantity = models.FloatField()
    value = models.FloatField()
