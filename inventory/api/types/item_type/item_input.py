from typing import Optional

from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from inventory.models import Item


@gql.django.input(Item)
class ItemCreateInput:
    name: str
    cost: float
    markup: float
    is_service: bool
    unit_of_measure: str
    category: auto


@gql.django.input(Item)
class ItemUpdateInput(gql.NodeInput):
    name: Optional[str]
    cost: Optional[float]
    markup: Optional[float]
    is_service: Optional[bool]
    unit_of_measure: Optional[str]
    category: Optional[gql.NodeInput]
