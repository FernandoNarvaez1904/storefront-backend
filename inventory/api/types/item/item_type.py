from abc import ABC
from typing import Optional

from strawberry import auto
from strawberry_django_plus import gql

from inventory.models import Item


@gql.django.type(model=Item)
class ItemType(gql.relay.Node, ABC):
    id: auto
    name: auto
    barcode: auto
    cost: auto
    markup: auto
    creation_date: auto
    is_active: auto
    current_stock: auto
    is_service: auto
    sku: auto

    @gql.django.field
    def price(self: Item) -> Optional[float]:
        try:
            cost = self.cost
            return cost + (cost * (self.markup / 100))
        except AttributeError:
            return None
