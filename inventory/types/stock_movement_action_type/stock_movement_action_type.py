import decimal
from abc import ABC
from datetime import datetime
from typing import Annotated

import strawberry

from inventory.models import StockMovementAction

ItemType_Lazy = Annotated["ItemType", strawberry.lazy("..item_type.item_type")]
from strawberry.relay import Node


@strawberry.django.type(StockMovementAction)
class StockMovementActionType(Node, ABC):
    item: ItemType_Lazy
    modification_amount: decimal.Decimal
    description: str
    item_cost: decimal.Decimal
    item_markup: decimal.Decimal
    item_price: decimal.Decimal
    creation_date: datetime
    document_type: str
