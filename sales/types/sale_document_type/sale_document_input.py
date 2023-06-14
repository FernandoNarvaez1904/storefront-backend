from typing import List, Optional

import strawberry
from strawberry_django_plus import gql

from company.types.payment_type.payment_input import PaymentCreateInput
from inventory.types.stock_movement_action_type.stock_movement_action_input import StockMovementActionCreateInput
from sales.models import SaleDocument


@gql.django.input(SaleDocument)
class SaleDocumentCreateInput:
    description: Optional[str] = strawberry.UNSET
    warehouse: gql.NodeInput
    client: gql.NodeInput
    stock_movements: List[StockMovementActionCreateInput]
    payments: List[PaymentCreateInput]
