from typing import List, cast

import strawberry

from inventory.api.mutations.item_activate.item_activate_errors import CannotActivateAlreadyActiveItem, \
    CannotActivateNonExistentItem

from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.types import UserError, InputTypeInterface
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list


@strawberry.input
class ItemActivateInput(InputTypeInterface):
    id: strawberry.ID = strawberry.field(description="The id given must be of an existing and inactive Item.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors: List[UserError] = []
        decoded_id: DecodedID = ItemType.decode_id(self.id)
        node_id = cast(str, decoded_id.get("instance_id"))
        item_list = await get_lazy_query_set_as_list(Item.objects.filter(id=node_id))

        if item_list:
            # As the filter was using id the resulting list will only have one result
            item = item_list[0]

            if item.is_active:
                errors.append(CannotActivateAlreadyActiveItem(
                    message=f"Item with id {self.id} is  active. Cannot activate active items"
                ))
        else:
            errors.append(
                CannotActivateNonExistentItem(message=f"Item with id {self.id} does not exist in database")
            )

        return errors
