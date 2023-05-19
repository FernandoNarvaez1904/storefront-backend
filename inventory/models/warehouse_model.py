from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    is_primary_warehouse = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_created=True)
    can_distribute = models.BooleanField(default=True)
