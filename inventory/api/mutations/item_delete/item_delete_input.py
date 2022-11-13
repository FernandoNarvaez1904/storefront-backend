from typing import List

import strawberry
from asgiref.sync import sync_to_async

from inventory.api.mutations.item_delete.item_delete_errors import CannotDeleteNonExistentItem, \
    CannotDeleteItemHasDocuments
from inventory.models import Item
from storefront_backend.api.relay.node import DecodedID, Node
from storefront_backend.api.types import UserError, InputTypeInterface


@strawberry.input
class ItemDeleteInput(InputTypeInterface):
    id: strawberry.ID = strawberry.field(description="The id given must be of an existing Item.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        decoded_id: DecodedID = Node.decode_id(self.id)
        node_id = decoded_id.get("instance_id")
        item_list = await sync_to_async(list)(Item.objects.filter(id=node_id))

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
