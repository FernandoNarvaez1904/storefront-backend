from abc import ABC
from typing import List

from django.contrib.auth.models import Permission
import strawberry

from users.models import Role


@strawberry.django.type(Permission)
class PermissionType(strawberry.relay.Node, ABC):
    name: str
    codename: str


@strawberry.django.type(Role)
class RoleType(strawberry.relay.Node, ABC):
    name: str
    permissions: List[PermissionType]
