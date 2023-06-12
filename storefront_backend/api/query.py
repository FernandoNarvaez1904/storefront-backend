from strawberry_django_plus import gql

from company.api.query import Query as CompanyDataQuery
from inventory.api.query import Query as InventoryQuery
from sales.api.query import Query as SalesQuery
from users.api.query import Query as UsersQuery


@gql.type
class Query(InventoryQuery, UsersQuery, CompanyDataQuery, SalesQuery):
    pass
