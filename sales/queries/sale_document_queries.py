import decimal
from typing import Optional

from strawberry_django_plus import gql

from sales.models import SaleDocument
from sales.types.sale_document_type.sale_document_filter import TotalSaleSearchFilter
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@gql.field
async def total_sales_amount(filter: Optional[TotalSaleSearchFilter] = None) -> decimal.Decimal:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    sales = SaleDocument.objects.filter(**filter_temp)
    return sum([sale.total async for sale in sales])
