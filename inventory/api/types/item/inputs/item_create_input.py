from typing import List

import strawberry
from strawberry import field

from inventory.api.types.item.user_error_types import BarcodeNotUniqueError, SKUNotUniqueError
from inventory.models import Item
from storefront_backend.api.types import UserError, InputTypeInterface


@strawberry.input
class ItemCreateInput(InputTypeInterface):
    sku: str = field(description="It must be unique")
    is_service: bool
    name: str
    barcode: str = field(description="It must be unique")
    cost: float
    markup: float

    async def validate_and_get_errors(self) -> List[UserError]:
        errors = []
        if await Item.objects.filter(sku=self.sku).aexists():
            errors.append(
                SKUNotUniqueError(
                    message="SKU is no unique"
                )
            )
        if await Item.objects.filter(barcode=self.barcode).aexists():
            errors.append(
                BarcodeNotUniqueError(
                    message="Barcode is no unique"
                )
            )
        return errors
