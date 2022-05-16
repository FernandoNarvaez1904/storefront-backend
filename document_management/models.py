from django.db import models


# Create your models here.
class Document(models.Model):
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
