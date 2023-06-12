from django.db import models

from documents.models import TransactionDocument


# Create your models here.
class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)


class Payment(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name="payments")
    amount = models.FloatField()
    document = models.ForeignKey(TransactionDocument, on_delete=models.PROTECT, related_name="payments")
