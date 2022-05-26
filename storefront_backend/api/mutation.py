from strawberry_django_plus import gql

from inventory.api.mutation import Mutation as InventoryMutation


@gql.type
class Mutation(InventoryMutation):
    pass
