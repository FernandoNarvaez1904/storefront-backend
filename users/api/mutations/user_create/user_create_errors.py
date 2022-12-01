import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotCreateUserUsernameIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "username"


@strawberry.type
class CannotCreateUserEmailIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "email"
