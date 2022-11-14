import strawberry

from inventory.api.mutation import Mutation as InventoryMutation
from users.api.mutation import Mutation as UserMutation


# ROOT
@strawberry.type
class Mutation(InventoryMutation, UserMutation):
    pass
