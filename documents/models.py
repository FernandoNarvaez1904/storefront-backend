# Create your models here.
from django.db import models


class Document(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    warehouse = models.ForeignKey("inventory.Warehouse", on_delete=models.PROTECT, related_name="documents")

    # TODO add reference number
