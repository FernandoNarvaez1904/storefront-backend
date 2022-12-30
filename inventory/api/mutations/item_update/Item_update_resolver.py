from typing import Optional, List

from django.db.models import Model

from inventory.api.mutations.item_update.item_update_input import ItemUpdateInput
from inventory.api.mutations.item_update.item_update_payload import ItemUpdatePayload
from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.utils import strawberry_mutation_resolver_payload
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list


@strawberry_mutation_resolver_payload(
    input_type=ItemUpdateInput,
    payload_type=ItemUpdatePayload,
    permission="inventory.change_item"
)
async def item_update_resolver(input, info) -> Optional[ItemType]:
    instance_id = ItemType.decode_id(input.id).get("instance_id")
    item: Item = await Item.objects.aget(id=instance_id)

    current_item_data = item.__dict__
    # _state is not a field in the ItemDetail model
    current_item_data.pop("_state")

    # Cleaning input data from None Fields
    input_data = {k: v for k, v in input.data.__dict__.items() if v and v != item.__getattribute__(k)}

    new_item: Optional[Model] = None
    if input_data:
        item_as_qs = Item.objects.filter(pk=item.id)
        await item_as_qs.aupdate(**input_data)
        temp: List[Model] = await get_lazy_query_set_as_list(item_as_qs)
        new_item = temp[0]

    if not new_item:
        return None

    return await ItemType.from_model_instance(new_item)
