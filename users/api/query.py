from strawberry_django import auth
from strawberry_django_plus import gql

from users.api.types.role_type.role_type import PermissionType, RoleType
from users.api.types.user_type.user_type import UserType


@gql.type
class Query:
    me: UserType = auth.current_user()
    user_connection: gql.Connection[UserType] = gql.django.connection()
    permission_connection: gql.Connection[PermissionType] = gql.django.connection()
    role_connection: gql.Connection[RoleType] = gql.django.connection()
