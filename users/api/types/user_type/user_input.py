from typing import Optional

import strawberry
from django.contrib.auth import get_user_model
from strawberry_django import ListInput, NodeInput


@strawberry.django.input(get_user_model())
class UserCreateInput:
    username: str = strawberry.UNSET
    first_name: str = strawberry.UNSET
    last_name: str = strawberry.UNSET
    email: str = strawberry.UNSET
    password: str = strawberry.UNSET


@strawberry.django.input(get_user_model())
class UserUpdateInput(NodeInput):
    username: str = strawberry.UNSET
    first_name: str = strawberry.UNSET
    last_name: str = strawberry.UNSET
    email: str = strawberry.UNSET


@strawberry.django.input(get_user_model())
class UserUpdatePasswordInput(NodeInput):
    password: str


@strawberry.django.input(get_user_model())
class UserAddRolesInput(NodeInput):
    roles: Optional[ListInput[NodeInput]]
