from typing import Optional

import strawberry

from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.relay.connection import get_cursor_page_from_queryset, get_connection_from_cursor_page, \
    Connection
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input



async def item_resolver(id:strawberry.ID) -> ItemType:
    qs =  await Item.objects.aget(id=id)
    
    return ItemType.from_model_instance(qs)