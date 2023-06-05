from strawberry_django_plus import gql

from strawberry_django_plus import gql

from inventory.models import Warehouse


@gql.django.input(Warehouse)
class WarehouseCreateInput:
    name: str
