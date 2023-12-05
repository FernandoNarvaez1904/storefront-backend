from abc import ABC

import strawberry

from sales.models import Client

from strawberry.relay import Node


@strawberry.django.type(Client)
class ClientType(Node, ABC):
    first_name: str
    last_name: str
