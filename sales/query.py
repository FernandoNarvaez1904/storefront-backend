from strawberry_django_plus import gql

from sales.queries.client_queries import client_connection
from sales.queries.sale_document_queries import total_sales_amount


@gql.type
class Query:
    client_connection = client_connection
    total_sales_amount = total_sales_amount
