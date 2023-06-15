from typing import Optional

from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto
from strawberry_django_plus.types import ListInput, NodeInput

from users.models import Role


@gql.django.input(Role)
class RoleCreateInput:
    name: str
    permissions: auto


@gql.django.input(Role)
class RoleUpdateInput(gql.NodeInput):
    name: Optional[str]
    permissions: Optional[ListInput[NodeInput]]
