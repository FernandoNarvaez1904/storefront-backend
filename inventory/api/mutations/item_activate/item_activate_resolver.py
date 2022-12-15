from asgiref.sync import sync_to_async

from inventory.api.mutations.item_activate.item_activate_input import ItemActivateInput
from inventory.api.mutations.item_activate.item_activate_payload import ItemActivatePayload
from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.utils import strawberry_mutation_resolver_payload


@strawberry_mutation_resolver_payload(
    input_type=ItemActivateInput,
    payload_type=ItemActivatePayload,
    permission="inventory.activate_item"
)
async def item_activate_resolver(input: ItemActivateInput, info) -> ItemType:
    instance_id = Node.decode_id(input.id).get("instance_id")
    item: Item = await Item.objects.aget(id=instance_id)
    item.is_active = True
    await sync_to_async(item.save)()
    return await ItemType.from_model_instance(item)
