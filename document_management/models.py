from django.db import models


# Create your models here.
class DocumentInterface(models.Model):
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
