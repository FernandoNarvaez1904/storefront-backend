from django.db import models

from documents.models import Document, TransactionDocument


# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ["first_name", "last_name"]


class SaleDocument(TransactionDocument):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="sale_documents")
