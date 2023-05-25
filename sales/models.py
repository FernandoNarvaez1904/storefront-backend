from django.db import models
from company.models import PaymentMethod
from document_management.models import DocumentInterface
from inventory.models import Client
from stock.models import StockModificationDocument


# Create your models here.
class SaleDocument(DocumentInterface):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    price_calculated = models.FloatField()
    is_paid = models.BooleanField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    sold_items = models.ManyToManyField(StockModificationDocument) 
