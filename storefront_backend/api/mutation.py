import strawberry
from strawberry_django_plus import gql

from inventory.api.mutation import Mutation as InventoryMutation


# ROOT
@strawberry.type
class Mutation(InventoryMutation):
    pass
