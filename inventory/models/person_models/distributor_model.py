from django.db import models

from inventory.models.interfaces import PersonInterface
from inventory.models.item_model import Item


class Distributor(PersonInterface):
    pass


class DistributorItemOffer(models.Model):
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="distributor_offer")
    cost = models.FloatField()

    class Meta:
        # Assures that every distributor has only one offer for item
        unique_together = ["distributor", "item"]
