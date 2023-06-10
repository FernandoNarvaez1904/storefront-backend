from abc import ABC
from datetime import datetime

from django.contrib.auth import get_user_model
from strawberry_django_plus import gql


@gql.django.type(get_user_model())
class UserType(gql.Node, ABC):
    username: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: datetime
