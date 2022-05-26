from typing import List

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.product.user_error_types import BarcodeNotUniqueError, SKUNotUniqueError
from inventory.models import Product, ProductDetail
from storefront_backend.api.types import UserError


@gql.django.input(Product)
class ProductCreateInput:
    sku: str
    is_service: bool
    name: str
    barcode: str
    cost: float
    markup: float

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        if await sync_to_async(Product.objects.filter(sku=self.sku).exists)():
            errors.append(
                SKUNotUniqueError(
                    message="SKU is no unique"
                )
            )
        if await sync_to_async(ProductDetail.objects.filter(barcode=self.barcode).exists)():
            errors.append(
                BarcodeNotUniqueError(
                    message="Barcode is no unique"
                )
            )
        return errors
