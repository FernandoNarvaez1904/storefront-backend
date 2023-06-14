from abc import ABC

from strawberry_django_plus import gql

from sales.models import Client


@gql.django.type(Client)
class ClientType(gql.NodeType, ABC):
    first_name: str
    last_name: str
