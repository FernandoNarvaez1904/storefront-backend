import strawberry

from inventory.api.mutation import Mutation as InventoryMutation


# ROOT
@strawberry.type
class Mutation(InventoryMutation):
    pass
