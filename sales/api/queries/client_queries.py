from typing import Optional, Iterable

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from sales.api.types.client_type.client_filter import ClientFilter
from sales.api.types.client_type.client_type import ClientType
from sales.models import Client
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@gql.relay.connection
async def client_connection(self, filter: Optional[ClientFilter] = None) -> Iterable[ClientType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    clients = Client.objects.filter(**filter_temp)
    await sync_to_async(len)(clients)
    return clients
