from typing import List, Optional

from strawberry_django_plus import gql

from storefront_backend.api.types import Payload, UserError
from .item_type import ItemType


@gql.type
class ItemCreatePayload(Payload):
    item: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class ItemDeactivatePayload(Payload):
    deactivated_item: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class ItemActivatePayload(Payload):
    activated_item: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class ItemUpdatePayload(Payload):
    update_item: Optional[ItemType]
    user_errors: List[UserError]
