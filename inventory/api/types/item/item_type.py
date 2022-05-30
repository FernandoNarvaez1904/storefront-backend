from abc import ABC
from datetime import datetime
from typing import Optional

from strawberry_django_plus import gql

from inventory.models import Item


@gql.django.type(Item)
class ItemType(gql.Node, ABC):
    id: gql.auto
    is_active: gql.auto
    current_stock: gql.auto
    is_service: gql.auto

    @gql.field
    def name(self: Item) -> Optional[str]:
        try:
            return self.current_detail.name
        except AttributeError:
            return None

    @gql.field
    def barcode(self: Item) -> Optional[str]:
        try:
            return self.current_detail.barcode
        except AttributeError:
            return None

    @gql.field
    def cost(self: Item) -> float:
        try:
            return self.current_detail.cost
        except AttributeError:
            return 0

    @gql.field
    def markup(self: Item) -> float:
        try:
            return self.current_detail.markup
        except AttributeError:
            return 0

    @gql.field
    def last_modified_date(self: Item) -> Optional[datetime]:
        try:
            return self.current_detail.date
        except AttributeError:
            return None

    @gql.field
    def sku(self: Item) -> Optional[str]:
        try:
            return self.current_detail.sku
        except AttributeError:
            return None

    @gql.field
    def price(self: Item) -> Optional[float]:
        try:
            cost = self.current_detail.cost
            return cost + (cost * (self.current_detail.markup / 100))
        except AttributeError:
            return None