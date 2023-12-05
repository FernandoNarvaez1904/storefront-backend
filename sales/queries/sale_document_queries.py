import decimal
from typing import Optional, Iterable

from asgiref.sync import sync_to_async
import strawberry

from sales.models import SaleDocument
from sales.types.sale_document_type.sale_document_filter import TotalSaleSearchFilter, SaleDocumentFilter
from sales.types.sale_document_type.sale_document_type import SaleDocumentType
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@strawberry.field
async def total_sales_amount(filter: Optional[TotalSaleSearchFilter] = None) -> decimal.Decimal:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    sales = SaleDocument.objects.filter(**filter_temp)
    return sum([sale.total async for sale in sales])


@strawberry.relay.connection(strawberry.relay.ListConnection[SaleDocumentType])
async def sale_document_connection(filter: Optional[SaleDocumentFilter] = None) -> Iterable[SaleDocumentType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    sales = SaleDocument.objects.filter(**filter_temp)
    await sync_to_async(len)(sales)
    return sales
