from typing import List, Optional

import strawberry
import strawberry

from company.types.payment_type.payment_input import PaymentCreateInput
from inventory.types.stock_movement_action_type.stock_movement_action_input import StockMovementActionCreateInput
from sales.models import SaleDocument
from strawberry_django import  NodeInput

@strawberry.django.input(SaleDocument)
class SaleDocumentCreateInput:
    description: Optional[str] = strawberry.UNSET
    warehouse: NodeInput
    client: NodeInput
    stock_movements: List[StockMovementActionCreateInput]
    payments: List[PaymentCreateInput]
