from abc import ABC
from typing import Annotated

import strawberry

from inventory.models import WarehouseStock

WareHouseType_Lazy = Annotated["WarehouseType", strawberry.lazy("..warehouse_type.warehouse_type")]
ItemType_Lazy = Annotated["ItemType", strawberry.lazy("..item_type.item_type")]


@strawberry.django.type(WarehouseStock)
class WarehouseStockType(strawberry.relay.Node, ABC):
    item: ItemType_Lazy
    warehouse: WareHouseType_Lazy
    stock_amount: float
