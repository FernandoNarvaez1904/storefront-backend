from typing import List

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ItemNotExistError
from inventory.api.types.item.user_error_types import ItemIsActiveError
from inventory.models import Item
from storefront_backend.api.types import UserError


@gql.django.input(Item)
class ItemActivateInput:
    id: gql.relay.GlobalID = gql.field(description="The id given must be of an existing and inactive Item.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        product_list = await sync_to_async(list)(Item.objects.filter(id=self.id.node_id))

        if product_list:
            # As the filter was using id the resulting list will only have one result
            item = product_list[0]

            if item.is_active:
                errors.append(ItemIsActiveError(
                    message=f"Item with id {self.id} is  active. Cannot activate inactive items"
                ))
        else:
            errors.append(
                ItemNotExistError(message=f"Item with id {self.id} does not exist in database")
            )

        return errors
