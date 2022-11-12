from typing import Optional

import strawberry
from strawberry_django.filters import FilterLookup

from storefront_backend.api.types import Filter


@strawberry.input
class ItemFilter(Filter):
    sku: Optional[FilterLookup[str]] = strawberry.UNSET
    name: Optional[FilterLookup[str]] = strawberry.UNSET
    cost: Optional[FilterLookup[float]] = strawberry.UNSET
    markup: Optional[FilterLookup[float]] = strawberry.UNSET
    is_active: Optional[bool] = strawberry.UNSET
    is_service: Optional[bool] = strawberry.UNSET
    current_stock: Optional[float] = strawberry.UNSET
