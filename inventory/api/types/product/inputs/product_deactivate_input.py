from typing import List

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.product import ProductNotExistError, ProductIsNotActive
from inventory.models import Product
from storefront_backend.api.types import UserError


@gql.django.input(Product)
class ProductDeactivateInput:
    id: gql.auto

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        product_list = await sync_to_async(list)(Product.objects.filter(id=self.id))
        
        if product_list:
            # As the filter was using id the resulting list will only have one result
            product = product_list[0]

            if not product.is_active:
                errors.append(ProductIsNotActive(
                    message=f"Product with id {self.id} is not active. Cannot deactivate inactive products"
                ))
        else:
            errors.append(
                ProductNotExistError(message=f"Product with id {self.id} does not exist in database")
            )

        return errors
