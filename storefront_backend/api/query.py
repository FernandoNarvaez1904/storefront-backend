import strawberry

from company.query import Query as CompanyDataQuery
from inventory.query import Query as InventoryQuery
from sales.query import Query as SalesQuery
from users.api.query import Query as UsersQuery


@strawberry.type
class Query(InventoryQuery, UsersQuery, CompanyDataQuery, SalesQuery):
    pass
