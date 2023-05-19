from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField()
    creation_date = models.DateTimeField(auto_created=True)
