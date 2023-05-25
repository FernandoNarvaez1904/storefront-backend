from typing import Optional, List
from strawberry_django_plus import gql
from sales.api.types.sale import SaleType
from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.types import UserError

@gql.type
class SaleCreatePayload(PayloadTypeInterface):
    node: Optional[SaleType]
    user_errors: List[UserError]