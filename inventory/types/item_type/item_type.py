import decimal
from abc import ABC
from datetime import datetime
from typing import List, Optional

from asgiref.sync import sync_to_async
import strawberry
from strawberry.relay import Node


from inventory.models import Item
from inventory.types.item_category_type.item_category_type import ItemCategoryType
from inventory.types.warehouse_stock_type.warehouse_stock_type import WarehouseStockType


@strawberry.django.type(Item, prefetch_related=["stock"])
class ItemType(Node, ABC):
    name: str
    cost: decimal.Decimal
    markup: decimal.Decimal
    price_c: decimal.Decimal
    creation_date: datetime
    is_service: bool
    category: Optional[ItemCategoryType]
    stock: strawberry.relay.ListConnection[WarehouseStockType] = strawberry.django.connection()

    @strawberry.field
    async def barcodes(self: Item) -> List[str]:
        bars = self.barcodes.all()
        await sync_to_async(len)(bars)
        return [bar.barcode for bar in bars]
