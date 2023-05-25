import strawberry

from .queries.item_connection.item_connection_resolver import item_connection_resolver
from .queries.item.item_resolver import item_resolver


@strawberry.type
class Query:
    item_connection = strawberry.field(item_connection_resolver)
    item = strawberry.field(item_resolver)
