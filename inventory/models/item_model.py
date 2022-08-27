from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ItemGroup(models.Model):
    name = models.CharField(max_length=255)
    group_parent = models.ForeignKey("ItemGroup", on_delete=models.CASCADE, related_name="group_children")


class Item(models.Model):
    name = models.CharField(max_length=255, default="")
    barcode = models.CharField(max_length=48, default="")
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    cost = models.FloatField(default=0)
    markup = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)
    is_service = models.BooleanField(default=False)
    sku = models.CharField(max_length=255, unique=True)
    current_stock = models.FloatField(default=0)
    group = models.ForeignKey(ItemGroup, on_delete=models.SET_NULL, null=True)
    current_detail = models.ForeignKey("ItemDetail", on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self.current_detail:
            self.name = self.current_detail.name
            self.barcode = self.current_detail.barcode
            self.cost = self.current_detail.cost
            self.markup = self.current_detail.markup
            self.creation_date = self.current_detail.date
        super(Item, self).save(*args, **kwargs)


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
