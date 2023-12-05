from typing import Optional

import strawberry
from strawberry_django import ListInput, NodeInput

from users.models import Role
from strawberry_django import NodeInput

@strawberry.django.input(Role)
class RoleCreateInput:
    name: str
    permissions: strawberry.auto


@strawberry.django.input(Role)
class RoleUpdateInput(NodeInput):
    name: Optional[str]
    permissions: Optional[ListInput[NodeInput]]
