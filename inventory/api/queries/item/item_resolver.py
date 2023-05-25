import strawberry

from inventory.api.types.item import ItemType
from inventory.models import Item


async def item_resolver(id: strawberry.ID) -> ItemType:
    item_id = ItemType.decode_id(id).get("instance_id")
    item: Item = await Item.objects.aget(id=item_id)
    return await ItemType.from_model_instance(item)
