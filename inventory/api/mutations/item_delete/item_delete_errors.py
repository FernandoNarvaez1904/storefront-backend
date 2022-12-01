import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotDeleteNonExistentItem(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "id"


@strawberry.type
class CannotDeleteItemHasDocuments(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "id"
