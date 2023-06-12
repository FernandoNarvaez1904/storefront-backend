from strawberry_django_plus import gql

from sales.api.queries.client_queries import client_connection


@gql.type
class Query:
    client_connection = client_connection
