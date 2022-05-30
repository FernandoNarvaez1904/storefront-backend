from typing import List, Optional

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ItemCreateInput, CreateProductPayload
from inventory.api.types.item.inputs.item_activate_input import ItemActivateInput
from inventory.api.types.item.inputs.item_deactivate_input import ItemDeactivateInput
from inventory.api.types.item.payload_types import DeactivateProductPayload, ActivateProductPayload
from inventory.models import Item, ItemDetail
from storefront_backend.api.types import UserError


@gql.type
class Mutation:

    @gql.field
    async def product_create(self, input: ItemCreateInput) -> CreateProductPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        prod: Optional[Item] = None
        if not errors:
            prod = await sync_to_async(Item.objects.create)(
                sku=input.sku,
            )
            await sync_to_async(ItemDetail.objects.create)(
                name=input.name,
                barcode=input.barcode,
                cost=input.cost,
                markup=input.markup,
                root_product=prod,
                is_service=input.is_service

            )
        return CreateProductPayload(product=prod, user_errors=errors)

    @gql.field
    async def product_deactivate(self, input: ItemDeactivateInput) -> DeactivateProductPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        prod: Optional[Item] = None
        if not errors:
            prod: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
            prod.is_active = False
            await sync_to_async(prod.save)()
        return DeactivateProductPayload(deactivated_product=prod, user_errors=errors)

    @gql.field
    async def product_activate(self, input: ItemActivateInput) -> ActivateProductPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        prod: Optional[Item] = None
        if not errors:
            prod: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
            prod.is_active = True
            await sync_to_async(prod.save)()
        return ActivateProductPayload(activated_product=prod, user_errors=errors)
