from asgiref.sync import sync_to_async

from inventory.api.mutations.item_deactivate.item_deactivate_input import ItemDeactivateInput
from inventory.api.mutations.item_deactivate.item_deactivate_payload import ItemDeactivatePayload
from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.utils import strawberry_mutation_resolver_payload


@strawberry_mutation_resolver_payload(
    input_type=ItemDeactivateInput,
    payload_type=ItemDeactivatePayload,
)
async def item_deactivate_resolver(input, info) -> ItemType:
    instance_id = Node.decode_id(input.id).get("instance_id")
    item: Item = await Item.objects.aget(id=instance_id)
    item.is_active = False
    await sync_to_async(item.save)()
    return ItemType.from_model_instance(item)
