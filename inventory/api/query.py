from strawberry_django_plus import gql

from inventory.api.queries.item_category_queries import items_category_connection
from inventory.api.queries.item_queries import items_connection


@gql.type
class Query:
    items_connection = items_connection
    items_category_connection = items_category_connection
