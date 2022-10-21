from typing import List

import strawberry
from asgiref.sync import sync_to_async

from inventory.api.types.item import ItemNotExistError, ItemIsNotActiveError
from inventory.models import Item
from storefront_backend.api.relay.node import DecodedID, Node
from storefront_backend.api.types import UserError, InputTypeInterface


@strawberry.input
class ItemDeactivateInput(InputTypeInterface):
    id: strawberry.ID = strawberry.field(description="The id given must be of an existing and active Item.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        decoded_id: DecodedID = Node.decode_id(self.id)
        node_id = decoded_id.get("instance_id")
        item_list = await sync_to_async(list)(Item.objects.filter(id=node_id))

        if item_list:
            # As the filter was using id the resulting list will only have one result
            item = item_list[0]

            if not item.is_active:
                errors.append(ItemIsNotActiveError(
                    message=f"Item with id {self.id} is not active. Cannot deactivate inactive items"
                ))
        else:
            errors.append(
                ItemNotExistError(message=f"item with id {self.id} does not exist in database")
            )

        return errors
