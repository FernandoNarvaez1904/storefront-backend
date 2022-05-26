from strawberry_django_plus import gql

from inventory.api.types.product import ProductType


@gql.type
class Query:
    product: ProductType = gql.relay.node()
    product_connection: gql.relay.Connection[ProductType] = gql.relay.connection()
