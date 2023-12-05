import decimal

import strawberry
from typing_extensions import Annotated

from inventory.models import StockMovementAction

WareHouseType_Lazy = Annotated["WarehouseType", strawberry.lazy("..warehouse_type.warehouse_type")]


@strawberry.django.input(StockMovementAction)
class StockMovementActionCreateInput:
    item: strawberry.auto
    modification_amount: decimal.Decimal
    description: str
