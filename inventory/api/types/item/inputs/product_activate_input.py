from typing import List

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ProductNotExistError
from inventory.api.types.item.user_error_types import ProductIsActiveError
from inventory.models import Item
from storefront_backend.api.types import UserError


@gql.django.input(Item)
class ProductActivateInput:
    id: gql.relay.GlobalID = gql.field(description="The id given must be of an existing and inactive Product.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        product_list = await sync_to_async(list)(Item.objects.filter(id=self.id.node_id))

        if product_list:
            # As the filter was using id the resulting list will only have one result
            product = product_list[0]

            if product.is_active:
                errors.append(ProductIsActiveError(
                    message=f"Product with id {self.id} is  active. Cannot activate inactive products"
                ))
        else:
            errors.append(
                ProductNotExistError(message=f"Product with id {self.id} does not exist in database")
            )

        return errors
