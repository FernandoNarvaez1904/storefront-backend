from asgiref.sync import sync_to_async

from inventory.api.mutations.item_update.item_update_input import ItemUpdateInput
from inventory.api.mutations.item_update.item_update_payload import ItemUpdatePayload
from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.utils import strawberry_mutation_resolver_payload


@strawberry_mutation_resolver_payload(
    input_type=ItemUpdateInput,
    payload_type=ItemUpdatePayload,
    returned_type=ItemType
)
async def item_update_resolver(input) -> ItemType:
    instance_id = Node.decode_id(input.id).get("instance_id")
    item: Item = await Item.objects.aget(id=instance_id)

    current_item_data = item.__dict__
    # _state is not a field in the ItemDetail model
    current_item_data.pop("_state")

    # Cleaning input data from None Fields
    input_data = {k: v for k, v in input.data.__dict__.items() if v and v != item.__getattribute__(k)}

    new_item = None
    if input_data:
        item_as_qs = Item.objects.filter(pk=item.id)
        await item_as_qs.aupdate(**input_data)
        l = await sync_to_async(list)(item_as_qs)
        new_item = l[0]

    return ItemType.from_model_instance(new_item)
