from typing import Iterable

from asgiref.sync import sync_to_async
from strawberry_django_plus import relay, gql

from inventory.api.types.item_type.item_type import ItemType
from inventory.models import Item


@gql.type
class Query:
    @relay.connection
    async def items_connection(self) -> Iterable[ItemType]:
        items = Item.objects.all()
        await sync_to_async(len)(items)
        return items
