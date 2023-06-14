import strawberry

from company.mutation import Mutation as CompanyDataMutation
from inventory.mutation import Mutation as InventoryMutation
from sales.mutation import Mutation as SalesMutation
from users.api.mutation import Mutation as UsersMutation


# ROOT
@strawberry.type
class Mutation(InventoryMutation, UsersMutation, CompanyDataMutation, SalesMutation):
    pass
