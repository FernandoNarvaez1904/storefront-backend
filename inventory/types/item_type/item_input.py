import decimal
from typing import Optional

from strawberry_django import NodeInput
import strawberry

from inventory.models import Item


@strawberry.django.input(Item)
class ItemCreateInput:
    name: str
    cost: decimal.Decimal
    markup: decimal.Decimal
    is_service: bool
    unit_of_measure: str
    category: strawberry.auto


@strawberry.django.input(Item)
class ItemUpdateInput(NodeInput):
    name: Optional[str]
    cost: Optional[decimal.Decimal]
    markup: Optional[decimal.Decimal]
    is_service: Optional[bool]
    unit_of_measure: Optional[str]
    category: Optional[NodeInput]
