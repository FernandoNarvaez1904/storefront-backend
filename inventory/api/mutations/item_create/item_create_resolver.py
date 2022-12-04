from inventory.api.mutations.item_create.item_create_input import ItemCreateInput
from inventory.api.mutations.item_create.item_create_payload import ItemCreatePayload
from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.utils import strawberry_mutation_resolver_payload


@strawberry_mutation_resolver_payload(
    input_type=ItemCreateInput,
    payload_type=ItemCreatePayload,
)
async def item_create_resolver(input, info) -> ItemType:
    item = await Item.objects.acreate(
        is_service=input.is_service,
        sku=input.sku,
        name=input.name,
        barcode=input.barcode,
        cost=input.cost,
        markup=input.markup,
    )
    return ItemType.from_model_instance(item)
