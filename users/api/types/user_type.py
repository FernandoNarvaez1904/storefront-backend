from datetime import datetime
from typing import Optional

import strawberry

from storefront_backend.api.relay.node import Node
from users.models import User


@strawberry.type
class UserType(Node):
    _model_ = User
    id: strawberry.ID
    username: str
    first_name: str
    last_name: str
    email: str
    is_superuser: bool
    is_staff: bool
    last_login: Optional[datetime]
    date_joined: datetime
    is_active: bool
