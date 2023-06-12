from typing import Optional

import strawberry
from strawberry_django_plus import gql

from sales.models import Client


@gql.django.input(Client)
class ClientCreateInput:
    first_name: str
    last_name: str


@gql.django.input(Client)
class ClientUpdateInput(gql.NodeInput):
    first_name: Optional[str] = strawberry.UNSET
    last_name: Optional[str] = strawberry.UNSET
