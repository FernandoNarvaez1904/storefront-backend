from typing import List, Optional

import strawberry

from storefront_backend.api.relay.node import Node
from storefront_backend.api.types import UserError


@strawberry.interface
class PayloadTypeInterface:
    user_errors: List[UserError]
    node: Optional[Node]
