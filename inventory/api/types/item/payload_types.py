from typing import List, Optional

from strawberry_django_plus import gql

from storefront_backend.api.types import Payload, UserError
from .item_type import ItemType


@gql.type
class CreateItemPayload(Payload):
    item: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class DeactivateProductPayload(Payload):
    deactivated_product: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class ActivateProductPayload(Payload):
    activated_product: Optional[ItemType]
    user_errors: List[UserError]
