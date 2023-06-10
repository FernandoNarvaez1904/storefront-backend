from abc import ABC
from datetime import datetime

from strawberry_django_plus import gql

from documents.models import Document
from inventory.api.types.warehouse_type.warehouse_type import WarehouseType


@gql.django.interface(Document)
class DocumentInterface(gql.Node, ABC):
    creation_date: datetime
    modification_date: datetime
    description: str
    warehouse: WarehouseType
