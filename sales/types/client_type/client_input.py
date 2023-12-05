from typing import Optional

import strawberry

from strawberry_django import  NodeInput

from sales.models import Client


@strawberry.django.input(Client)
class ClientCreateInput:
    first_name: str
    last_name: str


@strawberry.django.input(Client)
class ClientUpdateInput(NodeInput):
    first_name: Optional[str] = strawberry.UNSET
    last_name: Optional[str] = strawberry.UNSET
