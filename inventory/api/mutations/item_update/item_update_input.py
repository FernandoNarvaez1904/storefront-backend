from typing import List, Optional, cast

import strawberry

from inventory.api.mutations.item_update.item_update_errors import CannotUpdateItemSkuIsNotUnique, \
    CannotUpdateItemBarcodeIsNotUnique, CannotUpdateInactiveItem, CannotUpdateNonExistentItem, \
    CannotUpdateItemNameIsNotUnique
from inventory.models import Item
from storefront_backend.api.relay.node import DecodedID, Node
from storefront_backend.api.types import UserError, InputTypeInterface
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list


@strawberry.input
class ItemUpdateDataInput(InputTypeInterface):
    barcode: Optional[str] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET
    cost: Optional[float] = strawberry.UNSET
    markup: Optional[float] = strawberry.UNSET
    sku: Optional[str] = strawberry.UNSET


@strawberry.input
class ItemUpdateInput(InputTypeInterface):
    id: strawberry.ID = strawberry.field(description="The id given must be of an existing and active Item.")
    data: ItemUpdateDataInput

    async def validate_and_get_errors(self) -> List[UserError]:
        errors: List[UserError] = []
        decoded_id: DecodedID = Node.decode_id(self.id)
        node_id: str = cast(str, decoded_id.get("instance_id"))
        item_list = await get_lazy_query_set_as_list(Item.objects.filter(id=node_id))

        if item_list:
            # As the filter was using id the resulting list will only have one result
            item = item_list[0]

            if not item.is_active:
                errors.append(CannotUpdateInactiveItem(
                    message=f"Item with id {self.id} is not active. Cannot deactivate inactive items"
                ))

            if self.data.sku:
                if await Item.objects.filter(sku=self.data.sku).aexists():
                    errors.append(
                        CannotUpdateItemSkuIsNotUnique(
                            message="SKU is not unique"
                        )
                    )

            if self.data.barcode:
                if await Item.objects.filter(barcode=self.data.barcode).aexists():
                    errors.append(
                        CannotUpdateItemBarcodeIsNotUnique(
                            message="Barcode is not unique"
                        )
                    )
            if self.data.name:
                if await Item.objects.filter(name=self.data.name).aexists():
                    errors.append(
                        CannotUpdateItemNameIsNotUnique(
                            message="Name is not unique"
                        )
                    )
        else:
            errors.append(
                CannotUpdateNonExistentItem(message=f"item with id {self.id} does not exist in database")
            )

        return errors
