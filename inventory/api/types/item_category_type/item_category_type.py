from abc import ABC
from typing import Optional

from strawberry_django_plus import gql

from inventory.models import ItemCategory


@gql.django.type(ItemCategory)
class ItemCategoryType(gql.Node, ABC):
    name: str
    parent: Optional["ItemCategoryType"]
