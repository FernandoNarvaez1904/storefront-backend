from abc import ABC
from datetime import datetime
from typing import Optional

from strawberry import auto
from strawberry_django_plus import gql
from strawberry_django_plus.relay import GlobalID

from inventory.models import Item, ItemDetail


@gql.django.type(ItemDetail)
class ItemVersionType(gql.Node, ABC):
    id: auto
    name: auto
    barcode: auto
    cost: auto
    markup: auto


@gql.django.type(model=Item)
class ItemType(gql.relay.Node, ABC):
    id: auto
    is_active: auto
    current_stock: auto
    is_service: auto
    sku: auto
    item_versions: gql.relay.Connection["ItemVersionType"] = gql.relay.connection()

    @gql.django.field
    def name(self: Item) -> Optional[str]:
        try:
            return self.current_detail.name
        except AttributeError:
            return None

    @gql.django.field
    def barcode(self: Item) -> Optional[str]:
        try:
            return self.current_detail.barcode
        except AttributeError:
            return None

    @gql.django.field
    def cost(self: Item) -> float:
        try:
            return self.current_detail.cost
        except AttributeError:
            return 0

    @gql.django.field
    def markup(self: Item) -> float:
        try:
            return self.current_detail.markup
        except AttributeError:
            return 0

    @gql.django.field
    def creation_date(self: Item) -> Optional[datetime]:
        try:
            return self.current_detail.date
        except AttributeError:
            return None

    @gql.django.field
    def price(self: Item) -> Optional[float]:
        try:
            cost = self.current_detail.cost
            return cost + (cost * (self.current_detail.markup / 100))
        except AttributeError:
            return None

    @gql.django.field
    def version_id(self: Item) -> Optional[GlobalID]:
        try:
            return GlobalID(node_id=f"{self.current_detail.id}", type_name="ItemVersionType")
        except AttributeError:
            return None
