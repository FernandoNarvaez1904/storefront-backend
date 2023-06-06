import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto
from typing_extensions import Annotated

from inventory.models import StockMovementAction

WareHouseType_Lazy = Annotated["WarehouseType", strawberry.lazy("..warehouse_type.warehouse_type")]


@gql.django.input(StockMovementAction)
class StockMovementActionCreateInput:
    item: auto
    modification_amount: float
    description: str
