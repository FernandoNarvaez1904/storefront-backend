from django.db import models


class ItemCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("ItemCategory", on_delete=models.PROTECT)


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    cost = models.FloatField()
    markup = models.FloatField()
    price_c = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_service = models.BooleanField(default=False)
    unit_of_measure = models.CharField(max_length=255)
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT, null=True, blank=True)


class Barcode(models.Model):
    barcode = models.CharField(max_length=255, unique=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="barcodes")
