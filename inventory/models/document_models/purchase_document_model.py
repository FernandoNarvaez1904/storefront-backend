from django.db import models

from inventory.models.interfaces import ItemBasedDocumentInterface
from inventory.models.person_models.distributor_model import Distributor


class PurchaseDocument(ItemBasedDocumentInterface):
    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT, null=True)
