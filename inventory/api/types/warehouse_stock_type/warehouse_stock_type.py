from abc import ABC
from typing import Annotated

import strawberry
from strawberry_django_plus import gql

from inventory.models import WarehouseStock

WareHouseType_Lazy = Annotated["WarehouseType", strawberry.lazy("..warehouse_type.warehouse_type")]
ItemType_Lazy = Annotated["ItemType", strawberry.lazy("..item_type.item_type")]


@gql.django.type(WarehouseStock)
class WarehouseStockType(gql.Node, ABC):
    item: ItemType_Lazy
    warehouse: WareHouseType_Lazy
    stock_amount: float
