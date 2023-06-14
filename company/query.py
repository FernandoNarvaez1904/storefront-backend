from strawberry_django_plus import gql

from company.queries.payment_method_queries import payment_method_connection


@gql.type
class Query:
    payment_method_connection = payment_method_connection
