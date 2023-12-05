from typing import Optional, Iterable

from asgiref.sync import sync_to_async
import strawberry

from sales.models import Client
from sales.types.client_type.client_filter import ClientFilter
from sales.types.client_type.client_type import ClientType
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@strawberry.relay.connection(strawberry.relay.ListConnection[ClientType])
async def client_connection(self, filter: Optional[ClientFilter] = None) -> Iterable[ClientType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    clients = Client.objects.filter(**filter_temp)
    await sync_to_async(len)(clients)
    return clients
