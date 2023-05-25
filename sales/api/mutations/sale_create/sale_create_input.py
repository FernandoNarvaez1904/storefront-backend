from typing import List, cast
import strawberry
from sales.models import SaleDocument
from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.types import UserError, InputTypeInterface
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list
from inventory.models import Client
from sales.api.types.sale import PaymentMethodType, SaleType, StockModificationDocumentType

@strawberry.input
class SaleCreateInput(InputTypeInterface):
    client:Client
    price_calculated:float
    is_paid:bool
    payment_method:PaymentMethodType
    sold_items:List[StockModificationDocumentType]

    async def validate_and_get_errors(self) -> List[UserError]:
        error: List[UserError]=[]
        return error
       
    