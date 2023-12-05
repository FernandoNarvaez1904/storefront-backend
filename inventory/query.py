import strawberry

from inventory.queries.item_category_queries import items_category_connection
from inventory.queries.item_queries import items_connection
from inventory.queries.stock_recount_document_queries import stock_recount_document_connection
from inventory.queries.warehouse_queries import warehouse_connection
from inventory.types.item_type.item_type import ItemType


@strawberry.type
class Query:
    items_connection: strawberry.relay.ListConnection[ItemType] = items_connection
    items_category_connection = items_category_connection

    warehouse_connection = warehouse_connection
    stock_recount_document_connection = stock_recount_document_connection
