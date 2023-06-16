from typing import Optional

from strawberry_django_plus import gql

from sales.queries.client_queries import client_connection
from sales.queries.sale_document_queries import total_sales_amount, sale_document_connection
from sales.types.client_type.client_type import ClientType
from sales.types.sale_document_type.sale_document_type import SaleDocumentType


@gql.type
class Query:
    client_connection = client_connection
    client: ClientType = gql.relay.node()

    total_sales_amount = total_sales_amount
    sale_document: Optional[SaleDocumentType] = gql.relay.node()
    sale_document_connection = sale_document_connection
