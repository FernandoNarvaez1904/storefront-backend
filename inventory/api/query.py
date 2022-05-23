from strawberry_django_plus import gql

from inventory.api.types.product_type import ProductType


@gql.type
class Query:
    # TODO Create Test
    product: ProductType = gql.relay.node()
    # TODO Create Test
    product_connection: gql.relay.Connection[ProductType] = gql.relay.connection()
