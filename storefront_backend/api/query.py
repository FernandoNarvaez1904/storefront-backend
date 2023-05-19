import strawberry

from inventory.api.query import Query as InventoryQuery
from storefront_backend.api.relay.node import node_resolver, Node
from users.api.query import Query as UsersQuery


@strawberry.type
class Query(InventoryQuery, UsersQuery):
    node: Node = strawberry.field(resolver=node_resolver)
