from typing import Optional

from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from inventory.models import ItemDetail, Item
from storefront_backend.api.types import Filter


@gql.django.input(model=ItemDetail)
class ItemDetailFilter(Filter):
    name: Optional[FilterLookup[str]]
    barcode: Optional[FilterLookup[str]]
    cost: Optional[FilterLookup[float]]
    markup: Optional[FilterLookup[float]]


@gql.django.input(model=Item)
class ItemFilter(Filter):
    current_detail: Optional[ItemDetailFilter]
    sku: Optional[FilterLookup[str]]
    is_active: Optional[bool]
    is_service: Optional[bool]
    current_stock: Optional[float]
