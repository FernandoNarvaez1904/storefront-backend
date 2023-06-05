from django.db import models


class ItemCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("ItemCategory", on_delete=models.PROTECT, null=True, blank=True)
