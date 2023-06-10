from abc import ABC
from datetime import datetime
from typing import List

import strawberry
from strawberry_django_plus import gql
from typing_extensions import Annotated

from documents.api.types.document_interface.document_interface import DocumentInterface
from inventory.api.types.stock_movement_action_type.stock_movement_action_type import StockMovementActionType
from inventory.models import StockRecountDocument

WareHouseType_Lazy = Annotated["WarehouseType", strawberry.lazy("..warehouse_type.warehouse_type")]


@gql.django.type(StockRecountDocument)
class StockRecountDocumentType(DocumentInterface, ABC):
    creation_date: datetime
    modification_date: datetime
    description: str
    warehouse: WareHouseType_Lazy
    stock_movements: List[StockMovementActionType]
