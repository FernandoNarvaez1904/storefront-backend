from abc import ABC
from datetime import datetime
from typing import List, Optional

from strawberry_django_plus import gql

from inventory.models import Item, ModifyStockOrder


@gql.django.type(Item)
class ProductType(gql.Node, ABC):
    id: gql.auto
    sku: gql.auto
    is_active: gql.auto

    @gql.field
    def is_service(self: Item) -> Optional[bool]:
        try:
            return self.current_detail.is_service
        except AttributeError:
            return None

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
    def current_stock(self: Item) -> Optional[float]:
        stock_changes: List[ModifyStockOrder] = self.stock_changes.all()
        stock = 0
        for i in stock_changes:
            stock += i.quantity_modified
        return stock

    @gql.field
    def price(self: Item) -> Optional[float]:
        try:
            cost = self.current_detail.cost
            return cost + (cost * (self.current_detail.markup / 100))
        except AttributeError:
            return None
