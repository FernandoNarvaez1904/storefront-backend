from abc import ABC

from strawberry_django_plus import gql

from users.models import User


@gql.django.type(User)
class UserType(gql.Node, ABC):
    pass
