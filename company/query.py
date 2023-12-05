import strawberry

from company.queries.payment_method_queries import payment_method_connection


@strawberry.type
class Query:
    payment_method_connection = payment_method_connection
