import strawberry

from users.api.mutation import Mutation as UserMutation


# ROOT
@strawberry.type
class Mutation(UserMutation):
    pass
