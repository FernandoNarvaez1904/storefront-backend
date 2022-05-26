from typing import List, Optional

from strawberry_django_plus import gql

from inventory.api.types.product.product_type import ProductType
from storefront_backend.api.types import Payload, UserError


@gql.type
class CreateProductPayload(Payload):
    product: Optional[ProductType]
    user_errors: List[UserError]
