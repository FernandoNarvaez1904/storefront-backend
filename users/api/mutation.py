import strawberry

from users.api.mutations.user_create.user_create_resolver import user_create_resolver


@strawberry.type
class Mutation:
    user_create = strawberry.field(user_create_resolver)
