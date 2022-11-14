import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotCreateUserUsernameIsNotUnique(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "username"


@strawberry.type
class CannotCreateUserEmailIsNotUnique(UserError):
    message: str
    field: str

    @strawberry.field
    async def field(self):
        return "email"
