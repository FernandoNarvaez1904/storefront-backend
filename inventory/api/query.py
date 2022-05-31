from strawberry_django_plus import gql

from .types.item import ItemType


@gql.type
class Query:
    item: ItemType = gql.relay.node()
    item_connection: gql.relay.Connection[ItemType] = gql.relay.connection()
