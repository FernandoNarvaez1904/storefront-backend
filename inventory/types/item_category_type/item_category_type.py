from abc import ABC
from typing import Optional

import strawberry
from inventory.models import ItemCategory



@strawberry.django.type(ItemCategory)
class ItemCategoryType(strawberry.relay.Node, ABC):
    name: str
    parent: Optional["ItemCategoryType"]
