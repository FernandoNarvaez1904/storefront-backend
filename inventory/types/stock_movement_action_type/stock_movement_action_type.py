import decimal
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
    modification_amount: decimal.Decimal
    description: str
    item_cost: decimal.Decimal
    item_markup: decimal.Decimal
    item_price: decimal.Decimal
    creation_date: datetime
    document_type: str
