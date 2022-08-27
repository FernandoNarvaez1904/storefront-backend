from typing import Optional

from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from inventory.models import Item
from storefront_backend.api.types import Filter


@gql.django.input(model=Item)
class ItemFilter(Filter):
    sku: Optional[FilterLookup[str]]
    name: Optional[FilterLookup[str]]
    cost: Optional[FilterLookup[float]]
    markup: Optional[FilterLookup[float]]
    is_active: Optional[bool]
    is_service: Optional[bool]
    current_stock: Optional[float]
