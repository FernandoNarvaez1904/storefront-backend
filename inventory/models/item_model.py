from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ItemGroup(models.Model):
    name = models.CharField(max_length=255)
    group_parent = models.ForeignKey("ItemGroup", on_delete=models.CASCADE, related_name="group_children")


class Item(models.Model):
    is_active = models.BooleanField(default=True)
    is_service = models.BooleanField(default=False)
    sku = models.CharField(max_length=255, unique=True)
    current_stock = models.FloatField(default=0)
    group = models.ForeignKey(ItemGroup, on_delete=models.SET_NULL, null=True)
    current_detail = models.ForeignKey("ItemDetail", on_delete=models.SET_NULL, null=True)


class ItemDetail(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=48)
    cost = models.FloatField()
    markup = models.FloatField()
    root_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_versions")


@receiver(post_save, sender=ItemDetail)
def make_new_detail_current_detail(sender, instance: ItemDetail, **kwargs):
    root_item = instance.root_item
    root_item.current_detail = instance
    root_item.save()
