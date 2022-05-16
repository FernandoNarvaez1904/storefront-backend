from django.db import models

from document_management.models import Document
from inventory.models.product_model import Product


class ModifyStockDocument(Document):
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="stock_changes")
    quantity_modified = models.FloatField()


class InventoryDocument(Document):
    modified_products = models.ManyToManyField(ModifyStockDocument)


class LostAndDamagedDocument(Document):
    type_of_doc = models.CharField(max_length=3, choices=[
        ("LST", "Lost"),
        ("DMD", "Damaged")
    ])
    lost_products = models.ManyToManyField(ModifyStockDocument)
