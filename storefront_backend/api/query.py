from strawberry_django_plus import gql

from inventory.api.query import Query as InventoryQuery


@gql.type
class Query(InventoryQuery):
    pass
