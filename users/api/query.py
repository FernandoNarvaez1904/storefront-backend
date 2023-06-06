from strawberry_django import auth
from strawberry_django_plus import gql

from users.api.types.user_type.user_type import UserType


@gql.type
class Query:
    me: UserType = auth.current_user()
