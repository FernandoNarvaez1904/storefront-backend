from typing import List

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ItemNotExistError
from inventory.models import Item
from storefront_backend.api.types import UserError, InputTypeInterface


# TODO TEST
@gql.django.input(Item)
class ItemDeleteInput(InputTypeInterface):
    id: gql.relay.GlobalID = gql.field(description="The id given must be of an existing Item.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        item_list = await sync_to_async(list)(Item.objects.filter(id=self.id.node_id))

        if not item_list:
            errors.append(
                ItemNotExistError(message=f"item with id {self.id} does not exist in database")
            )

        return errors
