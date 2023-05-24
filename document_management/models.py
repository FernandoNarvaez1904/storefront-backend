from django.db import models

from inventory.models import Warehouse
from users.models import User


# Create your models here.
class DocumentInterface(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField(null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)

    class Meta:
        abstract = True
