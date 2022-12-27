import strawberry

from storefront_backend.api.types import UserError


@strawberry.type
class RoleDoesNotExistError(UserError):
    message: str

    @strawberry.field
    def field(self) -> str:
        return "role_id"


@strawberry.type
class UserDoesNotExistError(UserError):
    message: str

    @strawberry.field
    def field(self) -> str:
        return "usersIds"


@strawberry.type
class ListOfIDIsEmptyError(UserError):
    message: str

    @strawberry.field
    def field(self) -> str:
        return "permissionsIds"
