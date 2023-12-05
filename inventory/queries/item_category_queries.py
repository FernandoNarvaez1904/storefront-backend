from typing import Iterable, Optional

from asgiref.sync import sync_to_async
import strawberry

from inventory.models import ItemCategory
from inventory.types.item_category_type.item_category_filter import ItemCategoryFilter
from inventory.types.item_category_type.item_category_type import ItemCategoryType
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@strawberry.relay.connection(strawberry.relay.ListConnection[ItemCategoryType])
async def items_category_connection(self, filter: Optional[ItemCategoryFilter] = None) -> Iterable[ItemCategoryType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    items_category = ItemCategory.objects.filter(**filter_temp)
    await sync_to_async(len)(items_category)
    return items_category
