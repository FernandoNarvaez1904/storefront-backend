# Create your models here.
from django.db import models

from company.models import PaymentMethod
from document_management.models import DocumentInterface
from inventory.models import Distributor
from stock.models import StockModificationDocument


# Create your models here.
class PurchaseDocument(DocumentInterface):
    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT)
    cost_calculated = models.FloatField()
    is_paid = models.BooleanField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    purchased_items = models.ManyToManyField(StockModificationDocument)
