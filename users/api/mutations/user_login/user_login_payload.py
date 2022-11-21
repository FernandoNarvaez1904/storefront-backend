from typing import Optional, List

import strawberry

from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.types import UserError
from users.api.types.user_type import UserType


@strawberry.type
class UserLoginPayload(PayloadTypeInterface):
    node: Optional[UserType]
    user_errors: List[UserError]
