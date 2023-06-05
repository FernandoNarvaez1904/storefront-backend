from typing import Optional

from strawberry_django_plus import gql

from inventory.models import ItemCategory


@gql.django.input(ItemCategory)
class ItemCategoryCreateInput:
    name: str
    parent: Optional[gql.NodeInput]