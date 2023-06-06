import strawberry

from inventory.api.mutation import Mutation as InventoryMutation
from users.api.mutation import Mutation as UsersMutation


# ROOT
@strawberry.type
class Mutation(InventoryMutation, UsersMutation):
    pass
