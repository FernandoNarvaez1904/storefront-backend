import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class RoleDoesNotExistError(UserError):
    message: str

    @strawberry.field
    def field(self) -> str:
        return "role_id"


@strawberry.type
class PermissionDoesNotExistError(UserError):
    message: str

    @strawberry.field
    def field(self) -> str:
        return "permissionsIds"


@strawberry.type
class ListOfIDIsEmptyError(UserError):
    message: str

    @strawberry.field
    def field(self) -> str:
        return "permissionsIds"
