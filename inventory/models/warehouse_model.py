from django.db import models

from inventory.models import Item


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)


class WarehouseStock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="stock")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stock")
    stock_amount = models.FloatField()

    class Meta:
        unique_together = ('item', 'warehouse')
