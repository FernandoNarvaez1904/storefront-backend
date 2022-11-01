import strawberry
from asgiref.sync import sync_to_async

from inventory.api.types.item import ItemType
from inventory.api.types.item.inputs import ItemCreateInput, ItemDeactivateInput, ItemActivateInput, \
    ItemUpdateInput, \
    ItemDeleteInput
from inventory.api.types.item.payload_types import ItemActivatePayload, ItemDeactivatePayload, ItemCreatePayload, \
    ItemUpdatePayload, ItemDeletePayload
from inventory.models import Item
from storefront_backend.api.query import Node
from storefront_backend.api.utils import strawberry_mutation_payload


@strawberry.type
class Mutation:

    @strawberry_mutation_payload(
        input_type=ItemCreateInput,
        payload_type=ItemCreatePayload,
        returned_type=ItemType
    )
    async def item_create(self, input) -> ItemType:
        item = await Item.objects.acreate(
            is_service=input.is_service,
            sku=input.sku,
            name=input.name,
            barcode=input.barcode,
            cost=input.cost,
            markup=input.markup,
        )
        return ItemType.from_model_instance(item)

    @strawberry_mutation_payload(
        input_type=ItemDeactivateInput,
        payload_type=ItemDeactivatePayload,
        returned_type=ItemType
    )
    async def item_deactivate(self, input) -> ItemType:
        instance_id = Node.decode_id(input.id).get("instance_id")
        item: Item = await Item.objects.aget(id=instance_id)
        item.is_active = False
        await sync_to_async(item.save)()
        return ItemType.from_model_instance(item)

    @strawberry_mutation_payload(
        input_type=ItemActivateInput,
        payload_type=ItemActivatePayload,
        returned_type=ItemType
    )
    async def item_activate(self, input) -> ItemType:
        instance_id = Node.decode_id(input.id).get("instance_id")
        item: Item = await Item.objects.aget(id=instance_id)
        item.is_active = True
        await sync_to_async(item.save)()
        return ItemType.from_model_instance(item)

    @strawberry_mutation_payload(
        input_type=ItemUpdateInput,
        payload_type=ItemUpdatePayload,
        returned_type=ItemType
    )
    async def item_update(self, input) -> ItemType:
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

    @strawberry_mutation_payload(
        input_type=ItemDeleteInput,
        payload_type=ItemDeletePayload,
        returned_type=ItemType
    )
    async def item_delete(self, input) -> Node:
        instance_id = Node.decode_id(input.id).get("instance_id")
        item: Item = await Item.objects.aget(id=instance_id)
        await sync_to_async(item.delete)()
        return ItemType.from_model_instance(item)
