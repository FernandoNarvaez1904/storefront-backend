import decimal
from abc import ABC
from datetime import datetime

from strawberry_django_plus import gql

from documents.models import TransactionDocument
from documents.types.document_interface.document_interface import DocumentInterface
from inventory.types.warehouse_type.warehouse_type import WarehouseType


@gql.django.interface(TransactionDocument)
class TransactionDocumentInterface(DocumentInterface, ABC):
    creation_date: datetime
    modification_date: datetime
    description: str
    warehouse: WarehouseType
    total: decimal.Decimal
