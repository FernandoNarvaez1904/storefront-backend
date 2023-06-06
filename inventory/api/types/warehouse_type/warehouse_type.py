from abc import ABC
from datetime import datetime

from strawberry_django_plus import gql

from inventory.api.types.warehouse_stock_type.warehouse_stock_type import WarehouseStockType
from inventory.models import Warehouse


@gql.django.type(Warehouse)
class WarehouseType(gql.Node, ABC):
    name: str
    creation_date: datetime
    stock: gql.relay.Connection[WarehouseStockType] = gql.django.connection()
