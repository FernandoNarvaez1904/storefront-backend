from typing import List

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.product import ProductCreateInput, CreateProductPayload
from inventory.models import Product, ProductDetail
from storefront_backend.api.types import UserError


@gql.type
class Mutation:

    @gql.field
    async def product_create(self, input: ProductCreateInput) -> CreateProductPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        prod = None
        if not errors:
            prod = await sync_to_async(Product.objects.create)(
                sku=input.sku,
            )
            await sync_to_async(ProductDetail.objects.create)(
                name=input.name,
                barcode=input.barcode,
                cost=input.cost,
                markup=input.markup,
                root_product=prod,
                is_service=input.is_service

            )
        return CreateProductPayload(product=prod, user_errors=errors)
