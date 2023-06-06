from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender="inventory.Item")
def add_new_item_to_warehouses_stock(sender, instance: "Item", *args, **kwargs):
    already_exists_in_warehouses = instance.stock.all().exists()
    if not already_exists_in_warehouses:
        warehouses = Warehouse.objects.all()
        warehouses_stock = [
            WarehouseStock(item=instance, warehouse=warehouse, stock_amount=0)
            for warehouse in warehouses
        ]
        WarehouseStock.objects.bulk_create(warehouses_stock)


@receiver(post_save, sender="inventory.Warehouse")
def add_items_stock_to_new_warehouse(sender, instance: "Warehouse", *args, **kwargs):
    already_has_stock = instance.stock.all().exists()
    if not already_has_stock:
        items = Item.objects.all()
        warehouses_stock = [
            WarehouseStock(item=item, warehouse=instance, stock_amount=0)
            for item in items
        ]
        WarehouseStock.objects.bulk_create(warehouses_stock)
