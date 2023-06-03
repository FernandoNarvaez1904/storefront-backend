import strawberry

from storefront_backend.api.relay.node import node_resolver, Node
from users.api.query import Query as UsersQuery


@strawberry.type
class Query(UsersQuery):
    node: Node = strawberry.field(resolver=node_resolver)
