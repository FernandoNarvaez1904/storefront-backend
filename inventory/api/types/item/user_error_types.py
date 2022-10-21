import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class SKUNotUniqueError(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "sku"


@strawberry.type
class BarcodeNotUniqueError(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "barcode"


@strawberry.type
class ItemNotExistError(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "id"


@strawberry.type
class ItemIsNotActiveError(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "id"


@strawberry.type
class ItemIsActiveError(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "id"


@strawberry.type
class ItemAlreadyHasDocument(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "id"
