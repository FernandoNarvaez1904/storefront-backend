from storefront_backend.api.utils.strawberry_mutation_resolver_payload import UserHasNoPermission
from users.api.mutations.role_create.role_create_errors import CannotCreateRoleNameIsNotUnique, \
    CannotCreateRolePermissionDoesNotExist
from users.api.mutations.user_create.user_create_errors import CannotCreateUserUsernameIsNotUnique, \
    CannotCreateUserEmailIsNotUnique
from users.api.mutations.user_login.user_login_errors import CannotLoginPasswordIsNotCorrect, \
    CannotLoginUsernameDoesNotExist

exported_types = [
    CannotCreateUserUsernameIsNotUnique,
    CannotCreateUserEmailIsNotUnique,

    CannotLoginPasswordIsNotCorrect,
    CannotLoginUsernameDoesNotExist,

    CannotCreateRoleNameIsNotUnique,
    CannotCreateRolePermissionDoesNotExist,

    UserHasNoPermission,
]
