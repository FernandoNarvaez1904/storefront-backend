from typing import List, Optional

from strawberry_django_plus import gql

from storefront_backend.api.types import PayloadTypeInterface, UserError
from .item_type import ItemType


@gql.type
class ItemCreatePayload(PayloadTypeInterface):
    node: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class ItemDeactivatePayload(PayloadTypeInterface):
    node: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class ItemActivatePayload(PayloadTypeInterface):
    node: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class ItemUpdatePayload(PayloadTypeInterface):
    node: Optional[ItemType]
    user_errors: List[UserError]


@gql.type
class ItemDeletePayload(PayloadTypeInterface):
    node: Optional[gql.Node]
    user_errors: List[UserError]
