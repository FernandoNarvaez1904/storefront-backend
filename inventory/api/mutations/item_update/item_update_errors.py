import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotUpdateNonExistentItem(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "id"


@strawberry.type
class CannotUpdateInactiveItem(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "id"


@strawberry.type
class CannotUpdateItemSkuIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "sku"


@strawberry.type
class CannotUpdateItemBarcodeIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "barcode"


@strawberry.type
class CannotUpdateItemNameIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "name"
