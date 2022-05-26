from strawberry_django_plus import gql

from storefront_backend.api.types import UserError


@gql.type
class SKUNotUniqueError(UserError):
    message: str
    field: str

    @gql.field
    async def field(self):
        return "sku"


@gql.type
class BarcodeNotUniqueError(UserError):
    message: str
    field: str

    @gql.field
    async def field(self):
        return "barcode"
