from django.db import models

from inventory.models.item_category_model import ItemCategory


class Item(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(decimal_places=2, max_digits=12)
    markup = models.DecimalField(decimal_places=2, max_digits=12)
    price_c = models.DecimalField(decimal_places=2, default=0, max_digits=12)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_service = models.BooleanField(default=False)
    unit_of_measure = models.CharField(max_length=255)
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT, null=True, blank=True)


class Barcode(models.Model):
    barcode = models.CharField(max_length=255, unique=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="barcodes")
