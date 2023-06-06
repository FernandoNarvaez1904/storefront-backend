from abc import ABC
from datetime import datetime
from typing import Annotated

import strawberry
from strawberry_django_plus import gql

from inventory.models import StockMovementAction

ItemType_Lazy = Annotated["ItemType", strawberry.lazy("..item_type.item_type")]


@gql.django.type(StockMovementAction)
class StockMovementActionType(gql.Node, ABC):
    item: ItemType_Lazy
    modification_amount: float
    description: str
    item_cost: float
    item_markup: float
    item_price: float
    modification_cost_value: float
    modification_price_value: float
    creation_date: datetime
    document_type: str
