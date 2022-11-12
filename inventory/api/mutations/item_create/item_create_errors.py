import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotCreateItemSkuIsNotUnique(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "sku"


@strawberry.type
class CannotCreateItemBarcodeIsNotUnique(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "barcode"


@strawberry.type
class CannotCreateItemNameIsNotUnique(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "name"
