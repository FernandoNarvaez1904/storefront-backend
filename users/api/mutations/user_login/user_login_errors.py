import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotLoginUsernameDoesNotExist(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "username"


@strawberry.type
class CannotLoginPasswordIsNotCorrect(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "password"
