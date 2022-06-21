from strawberry_django_plus import gql

from storefront_backend.api.utils.filter_connection import filter_connection
from .types.item import ItemType
from .types.item.filters import ItemFilter


@gql.type
class Query:
    item: ItemType = gql.relay.node()
    item_connection = filter_connection(return_type=ItemType, filter_input=ItemFilter)
