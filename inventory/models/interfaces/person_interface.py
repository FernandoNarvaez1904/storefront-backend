from django.db import models


class PersonInterface(models.Model):
    name = models.CharField(max_length=255)
