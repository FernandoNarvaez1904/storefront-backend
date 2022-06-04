from typing import List, Optional

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ItemIsNotActiveError, ItemNotExistError
from inventory.models import Item, ItemDetail
from storefront_backend.api.types import UserError


@gql.django.input(ItemDetail)
class ItemUpdateDataInput:
    barcode: Optional[str]
    name: Optional[str]
    cost: Optional[float]
    markup: Optional[float]


@gql.django.input(Item)
class ItemUpdateInput:
    id: gql.relay.GlobalID = gql.field(description="The id given must be of an existing and active Item.")
    data: ItemUpdateDataInput

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        item_list = await sync_to_async(list)(Item.objects.filter(id=self.id.node_id))

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
