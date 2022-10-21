from typing import Optional

import strawberry

from storefront_backend.api.relay.connection import Connection, get_cursor_page_from_queryset, \
    get_connection_from_cursor_page
from storefront_backend.api.relay.node import Node
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input
from .types.item import ItemType
from .types.item.filters import ItemFilter
from ..models import Item


@strawberry.type
class Query:

    @strawberry.field
    async def item_connection(self, before: Optional[strawberry.ID] = None,
                              after: Optional[strawberry.ID] = None,
                              first: Optional[int] = None,
                              last: Optional[int] = None, filter: Optional[ItemFilter] = None) -> Connection[ItemType]:
        filt = await get_filter_arg_from_filter_input(filter)
        qs = Item.objects.filter(**filt)
        page = await get_cursor_page_from_queryset(qs, after, before, first, last)
        connection = await get_connection_from_cursor_page(page, ItemType)
        return connection

    @strawberry.field(deprecation_reason="Migration to only node")
    async def item(self, id: strawberry.ID) -> Optional[ItemType]:
        id_decoded = Node.decode_id(id)
        model_instance = await Item.objects.aget(pk=id_decoded.get("instance_id"))
        return ItemType.from_model_instance(model_instance)
