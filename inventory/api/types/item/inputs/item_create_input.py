from typing import List

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item.user_error_types import BarcodeNotUniqueError, SKUNotUniqueError
from inventory.models import Item, ItemDetail
from storefront_backend.api.types import UserError, InputTypeInterface
from strawberry import field


@gql.django.input(Item)
class ItemCreateInput(InputTypeInterface):
    sku: str = field(description="It must be unique")
    is_service: bool
    name: str
    barcode: str = field(description="It must be unique")
    cost: float
    markup: float

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        if await sync_to_async(Item.objects.filter(sku=self.sku).exists)():
            errors.append(
                SKUNotUniqueError(
                    message="SKU is no unique"
                )
            )
        if await sync_to_async(ItemDetail.objects.filter(barcode=self.barcode).exists)():
            errors.append(
                BarcodeNotUniqueError(
                    message="Barcode is no unique"
                )
            )
        return errors
