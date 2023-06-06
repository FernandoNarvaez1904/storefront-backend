from typing import Annotated, List

import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.types import NodeInput

from inventory.api.types.stock_movement_action_type.stock_movement_action_input import StockMovementActionCreateInput
from inventory.models import StockRecountDocument

WareHouseType_Lazy = Annotated["WarehouseType", strawberry.lazy("..warehouse_type.warehouse_type")]


@gql.django.input(StockRecountDocument)
class StockRecountDocumentCreateInput:
    description: str
    warehouse: NodeInput
    stock_movements: List[StockMovementActionCreateInput]
