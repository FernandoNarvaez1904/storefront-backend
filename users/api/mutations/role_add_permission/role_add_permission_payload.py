from typing import Optional, List

import strawberry

from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.types import UserError
from users.api.types.role_type import RoleType


@strawberry.type
class RoleAddPermissionPayload(PayloadTypeInterface):
    node: Optional[RoleType]
    user_errors: List[UserError]
