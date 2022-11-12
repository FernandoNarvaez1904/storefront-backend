import strawberry

from .queries.item_connection.item_connection_resolver import item_connection_resolver


@strawberry.type
class Query:
    item_connection = strawberry.field(item_connection_resolver)
