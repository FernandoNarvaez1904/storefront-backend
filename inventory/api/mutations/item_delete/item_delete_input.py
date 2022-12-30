from typing import List, cast

import strawberry

from inventory.api.mutations.item_delete.item_delete_errors import CannotDeleteNonExistentItem, \
    CannotDeleteItemHasDocuments
from inventory.api.types.item import ItemType
from inventory.models import Item
from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.types import UserError, InputTypeInterface
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list


@strawberry.input
class ItemDeleteInput(InputTypeInterface):
    id: strawberry.ID = strawberry.field(description="The id given must be of an existing Item.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors: List[UserError] = []
        decoded_id: DecodedID = ItemType.decode_id(self.id)
        node_id = cast(str, decoded_id.get("instance_id"))
        item_list = await get_lazy_query_set_as_list(Item.objects.filter(id=node_id))

        if not item_list:
            errors.append(
                CannotDeleteNonExistentItem(message=f"item with id {self.id} does not exist in database")
            )

        modify_stock_order_list = False
        if modify_stock_order_list:
            errors.append(
                CannotDeleteItemHasDocuments(
                    message=f"item with id {self.id} already has documents and cannot be deleted, you might want to "
                            f"deactivate instead.")
            )

        return errors
