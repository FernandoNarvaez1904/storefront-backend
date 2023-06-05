from strawberry_django_plus import gql

from inventory.models import Item


@gql.django.input(Item)
class ItemCreateInput:
    name: str
    cost: float
    markup: float
    price_c: float
    is_service: bool
    unit_of_measure: str
