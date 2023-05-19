from django.db import models


class Distributor(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    creation_date = models.DateTimeField(auto_created=True)
