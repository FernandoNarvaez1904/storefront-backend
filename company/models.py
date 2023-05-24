from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_created=True)
    # TODO mission logo


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
