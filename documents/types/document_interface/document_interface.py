from abc import ABC
from datetime import datetime

import strawberry
from strawberry.relay import Node

from documents.models import Document
from inventory.types.warehouse_type.warehouse_type import WarehouseType


@strawberry.django.interface(Document)
class DocumentInterface(Node, ABC):
    creation_date: datetime
    modification_date: datetime
    description: str
    warehouse: WarehouseType
