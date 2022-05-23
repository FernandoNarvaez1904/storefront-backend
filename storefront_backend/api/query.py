from typing import Optional

from strawberry_django_plus import gql
from inventory.api.query import Query as InventoryQuery


@gql.type
class Query(InventoryQuery):
    node: Optional[gql.Node] = gql.django.node()
