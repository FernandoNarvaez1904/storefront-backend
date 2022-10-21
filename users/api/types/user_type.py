from abc import ABC
from datetime import datetime

import strawberry
from strawberry import auto

from storefront_backend.api.relay.node import Node
from users.models import User


@strawberry.type
class UserType(Node):
    _model_ = User
    username: str
    first_name: str
    last_name: str
    email: str
    is_superuser: bool
    is_staff: bool
    last_login: datetime
    date_joined: datetime
    is_active: bool
