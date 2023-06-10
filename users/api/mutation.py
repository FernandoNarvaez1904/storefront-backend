from strawberry_django import auth
from strawberry_django_plus import gql

from users.api.types.user_type.user_input import UserCreateInput, UserUpdateInput
from users.api.types.user_type.user_type import UserType


@gql.type
class Mutation:
    login: UserType = auth.login()
    logout = auth.logout()
    register: UserType = auth.register(UserCreateInput)
    update_user: UserType = gql.django.update_mutation(UserUpdateInput)
