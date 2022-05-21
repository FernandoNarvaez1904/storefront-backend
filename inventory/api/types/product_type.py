from abc import ABC
from datetime import datetime
from enum import auto
from typing import List

from strawberry_django_plus import gql

from inventory.models import Product, ModifyStockDocument


@gql.django.type(Product)
class ProductType(gql.Node, ABC):
    id: auto
    sku: auto
    is_service: auto
    is_active: auto

    @gql.field
    def name(self: Product) -> str:
        return self.current_detail.name

    @gql.field
    def barcode(self: Product) -> str:
        return self.current_detail.barcode

    @gql.field
    def cost(self: Product) -> float:
        return self.current_detail.cost

    @gql.field
    def markup(self: Product) -> float:
        return self.current_detail.markup

    @gql.field
    def last_modified_date(self: Product) -> datetime:
        return self.current_detail.date

    @gql.field
    def current_stock(self: Product) -> float:
        stock_changes: List[ModifyStockDocument] = self.stock_changes.all()
        stock = 0
        for i in stock_changes:
            stock += i.quantity_modified
        return stock
