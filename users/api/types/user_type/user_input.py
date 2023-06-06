import strawberry
from django.contrib.auth import get_user_model
from strawberry_django_plus import gql


@gql.django.input(get_user_model())
class UserCreateInput:
    username: str = strawberry.UNSET
    first_name: str = strawberry.UNSET
    last_name: str = strawberry.UNSET
    email: str = strawberry.UNSET
    password: str = strawberry.UNSET


@gql.django.input(get_user_model())
class UserUpdateInput(gql.NodeInput):
    username: str = strawberry.UNSET
    first_name: str = strawberry.UNSET
    last_name: str = strawberry.UNSET
    email: str = strawberry.UNSET
