import strawberry

from company.api.mutation import Mutation as CompanyDataMutation
from inventory.api.mutation import Mutation as InventoryMutation
from users.api.mutation import Mutation as UsersMutation


# ROOT
@strawberry.type
class Mutation(InventoryMutation, UsersMutation, CompanyDataMutation):
    pass
