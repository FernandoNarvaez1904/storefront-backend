import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class CannotCreateRoleNameIsNotUnique(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "name"


@strawberry.type
class CannotCreateRolePermissionDoesNotExist(UserError):
    message: str

    @strawberry.field
    async def field(self) -> str:
        return "permissions_id"
