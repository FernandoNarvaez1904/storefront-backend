from __future__ import annotations

from typing import List

from inventory.models import Item


async def create_bulk_of_item(num: int, active: bool = True, seed: str = "") -> List[Item]:
    item_list = []
    for i in range(num):
        item = await Item.objects.acreate(
            sku=f"{seed}{i}", is_active=active, name=f"{seed}item{i}",
            barcode=f"{seed}barcode{i}",
            cost=10,
            markup=50,
        )
        item_list.append(item)
    return item_list
