from django.db import models


class ItemGroup(models.Model):
    name = models.CharField(max_length=255)
    group_parent = models.ForeignKey("ItemGroup", on_delete=models.CASCADE, related_name="group_children")


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    barcode = models.CharField(max_length=48, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    cost = models.FloatField(default=0)
    markup = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)
    is_service = models.BooleanField(default=False)
    sku = models.CharField(max_length=255, unique=True)
    current_stock = models.FloatField(default=0)
    group = models.ForeignKey(ItemGroup, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("activate_item", "Can Activate and Deactivate Items")
        ]
