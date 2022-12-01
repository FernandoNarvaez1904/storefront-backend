import strawberry

from inventory.api.query import Query as InventoryQuery
from storefront_backend.api.relay.node import node_resolver, Node


@strawberry.type
class Query(InventoryQuery):
    node: Node = strawberry.field(resolver=node_resolver)
