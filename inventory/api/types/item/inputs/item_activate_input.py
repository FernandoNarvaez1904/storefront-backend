from typing import List

import strawberry
from asgiref.sync import sync_to_async

from inventory.api.types.item import ItemIsActiveError
from inventory.api.types.item import ItemNotExistError
from inventory.models import Item
from storefront_backend.api.relay.node import Node, DecodedID
from storefront_backend.api.types import UserError, InputTypeInterface


@strawberry.input
class ItemActivateInput(InputTypeInterface):
    id: strawberry.ID = strawberry.field(description="The id given must be of an existing and inactive Item.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        decoded_id: DecodedID = Node.decode_id(self.id)
        node_id = decoded_id.get("instance_id")
        item_list = await sync_to_async(list)(Item.objects.filter(id=node_id))

        if item_list:
            # As the filter was using id the resulting list will only have one result
            item = item_list[0]

            if item.is_active:
                errors.append(ItemIsActiveError(
                    message=f"Item with id {self.id} is  active. Cannot activate active items"
                ))
        else:
            errors.append(
                ItemNotExistError(message=f"Item with id {self.id} does not exist in database")
            )

        return errors
