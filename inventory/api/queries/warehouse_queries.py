from typing import Optional, Iterable

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.warehouse_type.warehouse_filter import WarehouseFilter
from inventory.api.types.warehouse_type.warehouse_type import WarehouseType
from inventory.models import Warehouse
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@gql.relay.connection
async def warehouse_connection(self, filter: Optional[WarehouseFilter] = None) -> Iterable[WarehouseType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    warehouses = Warehouse.objects.filter(**filter_temp)
    await sync_to_async(len)(warehouses)
    return warehouses
