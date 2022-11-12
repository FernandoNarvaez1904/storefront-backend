import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotActivateAlreadyActiveItem(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "id"


@strawberry.type
class CannotActivateNonExistentItem(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "id"
