from typing import Optional, List

import strawberry

from inventory.api.types.item import ItemType
from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.types import UserError


@strawberry.type
class ItemCreatePayload(PayloadTypeInterface):
    node: Optional[ItemType]
    user_errors: List[UserError]
