from abc import ABC
from datetime import datetime

import strawberry

from inventory.models import Warehouse
from inventory.types.warehouse_stock_type.warehouse_stock_type import WarehouseStockType


@strawberry.django.type(Warehouse)
class WarehouseType(strawberry.relay.Node, ABC):
    name: str
    creation_date: datetime
    stock: strawberry.relay.ListConnection[WarehouseStockType] = strawberry.django.connection()
