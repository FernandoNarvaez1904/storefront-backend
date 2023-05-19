import strawberry

from .queries.user_connection.user_connection_resolver import user_connection_resolver


@strawberry.type
class Query:
    user_connection = strawberry.field(user_connection_resolver)
