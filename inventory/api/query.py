from strawberry_django_plus import gql

from .types.item import ItemType


@gql.type
class Query:
    product: ItemType = gql.relay.node()
    product_connection: gql.relay.Connection[ItemType] = gql.relay.connection()
