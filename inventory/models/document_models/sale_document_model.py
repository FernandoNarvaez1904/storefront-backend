from django.db import models

from inventory.models.interfaces import ItemBasedDocumentInterface
from inventory.models.person_models.customer_model import Customer


class SaleDocument(ItemBasedDocumentInterface):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
