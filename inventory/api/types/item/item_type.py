from datetime import datetime
from typing import Optional

import strawberry

from inventory.models import Item
from storefront_backend.api.relay.node import Node


@strawberry.type
class ItemType(Node):
    _model_ = Item
    id: strawberry.ID
    name: str
    barcode: str
    cost: float
    markup: float
    creation_date: datetime
    is_active: bool
    current_stock: int
    is_service: bool
    sku: str

    @strawberry.field
    def price(self) -> Optional[float]:
        try:
            cost = self.cost
            return cost + (cost * (self.markup / 100))
        except AttributeError:
            return None
