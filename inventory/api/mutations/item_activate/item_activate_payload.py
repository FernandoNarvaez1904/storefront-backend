from typing import Optional, List

from strawberry_django_plus import gql

from inventory.api.types.item import ItemType
from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.types import UserError


@gql.type
class ItemActivatePayload(PayloadTypeInterface):
    node: Optional[ItemType]
    user_errors: List[UserError]
