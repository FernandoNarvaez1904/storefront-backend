from strawberry_django_plus import gql

from inventory.api.mutation import Mutation as InventoryMutation


# ROOT
@gql.type
class Mutation(InventoryMutation):
    pass
