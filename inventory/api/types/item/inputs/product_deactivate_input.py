from typing import List

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ProductNotExistError, ProductIsNotActiveError
from inventory.models import Item
from storefront_backend.api.types import UserError


@gql.django.input(Item)
class ProductDeactivateInput:
    id: gql.relay.GlobalID = gql.field(description="The id given must be of an existing and active Product.")

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        product_list = await sync_to_async(list)(Item.objects.filter(id=self.id.node_id))

        if product_list:
            # As the filter was using id the resulting list will only have one result
            product = product_list[0]

            if not product.is_active:
                errors.append(ProductIsNotActiveError(
                    message=f"Product with id {self.id} is not active. Cannot deactivate inactive products"
                ))
        else:
            errors.append(
                ProductNotExistError(message=f"Product with id {self.id} does not exist in database")
            )

        return errors
