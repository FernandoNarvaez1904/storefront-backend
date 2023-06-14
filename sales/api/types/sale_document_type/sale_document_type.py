import decimal
from abc import ABC
from datetime import datetime
from typing import List

from strawberry_django_plus import gql

from company.api.types.payment_type.payment_type import PaymentType
from documents.api.types.transaction_document_interface.transaction_document_interface import \
    TransactionDocumentInterface
from inventory.api.types.stock_movement_action_type.stock_movement_action_type import StockMovementActionType
from inventory.api.types.warehouse_type.warehouse_type import WarehouseType
from sales.api.types.client_type.client_type import ClientType
from sales.models import SaleDocument


@gql.django.type(SaleDocument)
class SaleDocumentType(TransactionDocumentInterface, ABC):
    creation_date: datetime
    modification_date: datetime
    description: str
    warehouse: WarehouseType
    total: decimal.Decimal
    client: ClientType
    payments: List[PaymentType]
    stock_movements: List[StockMovementActionType]
