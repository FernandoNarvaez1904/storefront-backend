import strawberry

from inventory.models import Warehouse
from strawberry_django import  NodeInput


@strawberry.django.input(Warehouse)
class WarehouseCreateInput:
    name: str


@strawberry.django.input(Warehouse)
class WarehouseUpdateInput(NodeInput):
    name: str
