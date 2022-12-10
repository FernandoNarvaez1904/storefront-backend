import strawberry

from users.api.mutations.role_create.role_create_resolver import role_create_resolver
from users.api.mutations.user_create.user_create_resolver import user_create_resolver
from users.api.mutations.user_login.user_login_resolver import user_login_resolver


@strawberry.type
class Mutation:
    user_create = strawberry.field(user_create_resolver)
    user_login = strawberry.field(user_login_resolver)

    role_create = strawberry.field(role_create_resolver)
