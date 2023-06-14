from strawberry_django_plus import gql

from inventory.models import Warehouse


@gql.django.input(Warehouse)
class WarehouseCreateInput:
    name: str


@gql.django.input(Warehouse)
class WarehouseUpdateInput(gql.NodeInput):
    name: str
