from typing import Optional

import strawberry

from inventory.models import ItemCategory

from strawberry_django import NodeInput

@strawberry.django.input(ItemCategory)
class ItemCategoryCreateInput:
    name: str
    parent: Optional[NodeInput]


@strawberry.django.input(ItemCategory)
class ItemCategoryUpdateInput(NodeInput):
    name: Optional[str]
    parent: Optional[NodeInput]
