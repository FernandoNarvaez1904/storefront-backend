from typing import Optional

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input
from .types.item import ItemType
from .types.item.filters import ItemFilter
from ..models import Item


@gql.type
class Query:
    item: ItemType = gql.relay.node()

    @gql.connection
    async def item_connection(self, filter: Optional[ItemFilter] = None) -> gql.Connection[ItemType]:
        filt = await get_filter_arg_from_filter_input(filter)
        qs = Item.objects.filter(**filt).prefetch_related("current_detail")
        await sync_to_async(len)(qs)
        return qs
