from abc import ABC
from datetime import datetime

from strawberry_django_plus import gql

from inventory.models import Warehouse


@gql.django.type(Warehouse)
class WarehouseType(gql.Node, ABC):
    name: str
    creation_date: datetime
