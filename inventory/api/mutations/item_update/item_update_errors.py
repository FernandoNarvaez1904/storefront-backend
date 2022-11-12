import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotUpdateNonExistentItem(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "id"


@strawberry.type
class CannotUpdateInactiveItem(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "id"


@strawberry.type
class CannotUpdateItemSkuIsNotUnique(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "sku"


@strawberry.type
class CannotUpdateItemBarcodeIsNotUnique(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "barcode"


@strawberry.type
class CannotUpdateItemNameIsNotUnique(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "name"
