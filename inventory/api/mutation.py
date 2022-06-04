from typing import List, Optional

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ItemCreateInput, CreateItemPayload
from inventory.api.types.item.inputs.item_activate_input import ItemActivateInput
from inventory.api.types.item.inputs.item_deactivate_input import ItemDeactivateInput
from inventory.api.types.item.inputs.item_update_input import ItemUpdateInput
from inventory.api.types.item.payload_types import DeactivateItemPayload, ActivateItemPayload, UpdateItemPayload
from inventory.models import Item, ItemDetail
from storefront_backend.api.types import UserError


@gql.type
class Mutation:

    @gql.field
    async def item_create(self, input: ItemCreateInput) -> CreateItemPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        item: Optional[Item] = None
        if not errors:
            item = await sync_to_async(Item.objects.create)(
                is_service=input.is_service,
                sku=input.sku,
            )
            await sync_to_async(ItemDetail.objects.create)(
                name=input.name,
                barcode=input.barcode,
                cost=input.cost,
                markup=input.markup,
                root_item=item,

            )
        return CreateItemPayload(item=item, user_errors=errors)

    @gql.field
    async def item_deactivate(self, input: ItemDeactivateInput) -> DeactivateItemPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        item: Optional[Item] = None
        if not errors:
            item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
            item.is_active = False
            await sync_to_async(item.save)()
        return DeactivateItemPayload(deactivated_item=item, user_errors=errors)

    @gql.field
    async def item_activate(self, input: ItemActivateInput) -> ActivateItemPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        item: Optional[Item] = None
        if not errors:
            item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
            item.is_active = True
            await sync_to_async(item.save)()
        return ActivateItemPayload(activated_item=item, user_errors=errors)

    @gql.field
    async def item_update(self, input: ItemUpdateInput) -> UpdateItemPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        item: Optional[Item] = None
        if not errors:
            item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)

            current_item_detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(id=item.current_detail_id)
            current_item_detail_data = current_item_detail.__dict__
            # _state is not a field in the ItemDetail model
            current_item_detail_data.pop("_state")

            # Cleaning input data from None Fields
            input_data = {k: v for k, v in input.data.__dict__.items() if v}

            if input_data:
                new_detail_data = {
                    **current_item_detail_data,
                    "id": None,
                    "date": None,
                    **input_data,
                }
                detail = await sync_to_async(ItemDetail.objects.create)(**new_detail_data)
                # this is needed because the signal is not fast enough
                item.current_detail = detail

        return UpdateItemPayload(update_item=item, user_errors=errors)
