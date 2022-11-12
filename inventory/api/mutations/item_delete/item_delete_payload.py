from typing import Optional, List

from strawberry_django_plus import gql

from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.types import UserError


@gql.type
class ItemDeletePayload(PayloadTypeInterface):
    node: Optional[gql.Node]
    user_errors: List[UserError]
