import strawberry
from django.contrib.auth.models import Permission

from storefront_backend.api.relay.node import Node


@strawberry.type
class PermissionType(Node):
    _model_ = Permission
    id: strawberry.ID
    name: str
    codename: str
