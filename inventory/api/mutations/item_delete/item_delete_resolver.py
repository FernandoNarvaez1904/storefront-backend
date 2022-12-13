from asgiref.sync import sync_to_async

from inventory.api.mutations.item_delete.item_delete_input import ItemDeleteInput
from inventory.api.mutations.item_delete.item_delete_payload import ItemDeletePayload
from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.utils import strawberry_mutation_resolver_payload


@strawberry_mutation_resolver_payload(
    input_type=ItemDeleteInput,
    payload_type=ItemDeletePayload,
    permission="inventory.delete_item"
)
async def item_delete_resolver(input, info) -> Node:
    instance_id = Node.decode_id(input.id).get("instance_id")
    item: Item = await Item.objects.aget(id=instance_id)
    await sync_to_async(item.delete)()

    item_deleted = await ItemType.from_model_instance(item)
    item_deleted.id = input.id
    return item_deleted
