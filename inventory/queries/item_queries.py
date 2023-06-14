from typing import Optional, Iterable

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.models import Item
from inventory.types.item_type.item_filter import ItemFilter
from inventory.types.item_type.item_type import ItemType
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@gql.relay.connection
async def items_connection(self, filter: Optional[ItemFilter] = None) -> Iterable[ItemType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    items = Item.objects.filter(**filter_temp)
    await sync_to_async(len)(items)
    return items
