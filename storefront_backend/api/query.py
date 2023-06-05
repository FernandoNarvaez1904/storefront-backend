from typing import List

import strawberry
from strawberry_django_plus import relay, gql

from inventory.api.types.item_type.item_type import ItemType


@strawberry.type
class Query:
    items_connection: relay.Connection[ItemType] = relay.connection()
    items: List[ItemType] = gql.django.field()
