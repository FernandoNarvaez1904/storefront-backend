from strawberry_django import auth
import strawberry

from users.api.types.role_type.role_type import PermissionType, RoleType
from users.api.types.user_type.user_type import UserType


@strawberry.type
class Query:
    me: UserType = auth.current_user()
    user_connection: strawberry.relay.ListConnection[UserType] = strawberry.django.connection()
    permission_connection: strawberry.relay.ListConnection[PermissionType] = strawberry.django.connection()
    role_connection: strawberry.relay.ListConnection[RoleType] = strawberry.django.connection()
