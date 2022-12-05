import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class UserHasNoPermission(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "permission"
