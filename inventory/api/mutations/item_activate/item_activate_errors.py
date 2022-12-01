import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotActivateAlreadyActiveItem(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "id"


@strawberry.type
class CannotActivateNonExistentItem(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "id"
