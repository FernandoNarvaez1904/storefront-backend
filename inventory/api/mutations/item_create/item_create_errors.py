import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotCreateItemSkuIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "sku"


@strawberry.type
class CannotCreateItemBarcodeIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "barcode"


@strawberry.type
class CannotCreateItemNameIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "name"
