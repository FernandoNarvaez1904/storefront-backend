from typing import Iterable, Optional

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.models import StockRecountDocument
from inventory.types.stock_recount_document_type.stock_recount_document_filter import StockRecountDocumentFilter
from inventory.types.stock_recount_document_type.stock_recount_document_type import StockRecountDocumentType
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@gql.relay.connection
async def stock_recount_document_connection(self, filter: Optional[StockRecountDocumentFilter] = None) -> Iterable[
    StockRecountDocumentType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    stock_recount_documents = StockRecountDocument.objects.filter(**filter_temp)
    await sync_to_async(len)(stock_recount_documents)
    return stock_recount_documents
