import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotDeactivateNonExistentItem(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "id"


@strawberry.type
class CannotDeactivateInactiveItem(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "id"
