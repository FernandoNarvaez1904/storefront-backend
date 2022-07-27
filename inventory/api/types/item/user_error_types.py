from strawberry_django_plus import gql

from storefront_backend.api.types import UserError


@gql.type
class SKUNotUniqueError(UserError):
    message: str
    field: str

    @gql.django.field
    async def field(self):
        return "sku"


@gql.type
class BarcodeNotUniqueError(UserError):
    message: str
    field: str

    @gql.django.field
    async def field(self):
        return "barcode"


@gql.type
class ItemNotExistError(UserError):
    message: str
    field: str

    @gql.django.field
    async def field(self):
        return "id"


@gql.type
class ItemIsNotActiveError(UserError):
    message: str
    field: str

    @gql.django.field
    async def field(self):
        return "id"


@gql.type
class ItemIsActiveError(UserError):
    message: str
    field: str

    @gql.django.field
    async def field(self):
        return "id"


@gql.type
class ItemAlreadyHasDocument(UserError):
    message: str
    field: str

    @gql.django.field
    async def field(self):
        return "id"
