from django.db import models

from document_management.models import DocumentInterface
from inventory.models.document_models.modify_stock_order_model import ModifyStockOrder


class ItemBasedDocumentInterface(DocumentInterface):
    items = models.ManyToManyField(ModifyStockOrder)
    total_value = models.FloatField()

    class Meta:
        abstract = True
