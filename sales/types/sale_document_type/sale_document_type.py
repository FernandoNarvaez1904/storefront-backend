import decimal
from abc import ABC
from datetime import datetime
from typing import List

import strawberry

from company.types.payment_type.payment_type import PaymentType
from documents.types.transaction_document_interface.transaction_document_interface import \
    TransactionDocumentInterface
from inventory.types.stock_movement_action_type.stock_movement_action_type import StockMovementActionType
from inventory.types.warehouse_type.warehouse_type import WarehouseType
from sales.models import SaleDocument
from sales.types.client_type.client_type import ClientType


@strawberry.django.type(SaleDocument)
class SaleDocumentType(TransactionDocumentInterface, ABC):
    creation_date: datetime
    modification_date: datetime
    description: str
    warehouse: WarehouseType
    total: decimal.Decimal
    client: ClientType
    payments: List[PaymentType]
    stock_movements: List[StockMovementActionType]
