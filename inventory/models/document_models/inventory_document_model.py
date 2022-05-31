from django.db import models

from inventory.models.interfaces import ItemBasedDocumentInterface


class InventoryDocument(ItemBasedDocumentInterface):
    kind = models.CharField(max_length=3, choices=[
        ("IVT", "Inventory"),
        ("DGD", "Damaged"),
        ("LST", "Lost")
    ])
