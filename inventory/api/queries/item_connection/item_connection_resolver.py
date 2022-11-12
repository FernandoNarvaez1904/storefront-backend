from typing import Optional

import strawberry

from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.relay.connection import get_cursor_page_from_queryset, get_connection_from_cursor_page, \
    Connection
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input
from .item_connection_filter import ItemFilter


async def item_connection_resolver(
        before: Optional[strawberry.ID] = None,
        after: Optional[strawberry.ID] = None,
        first: Optional[int] = None,
        last: Optional[int] = None, filter: Optional[ItemFilter] = None) -> Connection[
    ItemType]:
    filt = await get_filter_arg_from_filter_input(filter)
    qs = Item.objects.filter(**filt)
    page = await get_cursor_page_from_queryset(qs, after, before, first, last)
    connection = await get_connection_from_cursor_page(page, ItemType)
    return connection
