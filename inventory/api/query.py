from typing import Optional

from strawberry_django_plus import gql

from inventory.api.types.product_type import ProductType


@gql.type
class Query:
    product: Optional[ProductType] = gql.relay.node()
    product_connection: gql.relay.Connection[ProductType] = gql.relay.connection()
