import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotLoginUsernameDoesNotExist(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "username"


@strawberry.type
class CannotLoginPasswordIsNotCorrect(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "password"
