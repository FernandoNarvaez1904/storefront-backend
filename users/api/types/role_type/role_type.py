from abc import ABC
from typing import List

from django.contrib.auth.models import Permission
from strawberry_django_plus import gql

from users.models import Role


@gql.django.type(Permission)
class PermissionType(gql.Node, ABC):
    name: str
    codename: str


@gql.django.type(Role)
class RoleType(gql.Node, ABC):
    name: str
    permissions: List[PermissionType]
