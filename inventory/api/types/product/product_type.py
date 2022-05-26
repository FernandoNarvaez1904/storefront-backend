from abc import ABC
from datetime import datetime
from typing import List, Optional

from strawberry_django_plus import gql

from inventory.models import Product, ModifyStockDocument


@gql.django.type(Product)
class ProductType(gql.Node, ABC):
    id: gql.auto
    sku: gql.auto
    is_service: gql.auto
    is_active: gql.auto

    @gql.field
    def name(self: Product) -> Optional[str]:
        try:
            return self.current_detail.name
        except AttributeError:
            return None

    @gql.field
    def barcode(self: Product) -> Optional[str]:
        try:
            return self.current_detail.barcode
        except AttributeError:
            return None

    @gql.field
    def cost(self: Product) -> float:
        try:
            return self.current_detail.cost
        except AttributeError:
            return 0

    @gql.field
    def markup(self: Product) -> float:
        try:
            return self.current_detail.markup
        except AttributeError:
            return 0

    @gql.field
    def last_modified_date(self: Product) -> Optional[datetime]:
        try:
            return self.current_detail.date
        except AttributeError:
            return None

    @gql.field
    def current_stock(self: Product) -> Optional[float]:
        stock_changes: List[ModifyStockDocument] = self.stock_changes.all()
        stock = 0
        for i in stock_changes:
            stock += i.quantity_modified
        return stock
