import strawberry

from users.api.mutations.role_add_permission.role_add_permission_resolver import role_add_permission_resolver
from users.api.mutations.role_add_users.role_add_users_resolver import role_add_users_resolver
from users.api.mutations.role_create.role_create_resolver import role_create_resolver
from users.api.mutations.role_remove_permission.role_remove_permission_resolver import role_remove_permission_resolver
from users.api.mutations.role_remove_users.role_remove_users_resolver import role_remove_users_resolver
from users.api.mutations.user_create.user_create_resolver import user_create_resolver
from users.api.mutations.user_login.user_login_resolver import user_login_resolver


@strawberry.type
class Mutation:
    user_create = strawberry.field(user_create_resolver)
    user_login = strawberry.field(user_login_resolver)

    role_create = strawberry.field(role_create_resolver)
    role_add_permission = strawberry.field(role_add_permission_resolver)
    role_remove_permission = strawberry.field(role_remove_permission_resolver)
    role_add_users = strawberry.field(role_add_users_resolver)
    role_remove_users = strawberry.field(role_remove_users_resolver)
