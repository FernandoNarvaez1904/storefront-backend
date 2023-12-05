from typing import Optional

import strawberry

from sales.queries.client_queries import client_connection
from sales.queries.sale_document_queries import total_sales_amount, sale_document_connection
from sales.types.client_type.client_type import ClientType
from sales.types.sale_document_type.sale_document_type import SaleDocumentType


@strawberry.type
class Query:
    client_connection = client_connection
    client: ClientType = strawberry.relay.node()

    total_sales_amount = total_sales_amount
    sale_document: Optional[SaleDocumentType] = strawberry.relay.node()
    sale_document_connection = sale_document_connection
