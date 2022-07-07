from abc import ABC

from strawberry import auto
from strawberry_django_plus import gql

from users.models import User


@gql.django.type(User)
class UserType(gql.Node, ABC):
    username: auto
    first_name: auto
    last_name: auto
    email: auto
    is_superuser: auto
    is_staff: auto
    last_login: auto
