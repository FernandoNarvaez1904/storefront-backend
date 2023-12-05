from datetime import datetime
from typing import Optional

import strawberry
from strawberry_django.filters import FilterLookup

from storefront_backend.api.types import Filter


@strawberry.input
class TotalSaleSearchFilter(Filter):
    creation_date: Optional[FilterLookup[datetime]] = strawberry.UNSET
    warehouse: Optional[FilterLookup[strawberry.relay.GlobalID]] = strawberry.UNSET
    client: Optional[FilterLookup[strawberry.relay.GlobalID]] = strawberry.UNSET
    description: Optional[str] = strawberry.UNSET


@strawberry.input
class SaleDocumentFilter(Filter):
    creation_date: Optional[FilterLookup[datetime]] = strawberry.UNSET
    modification_date: Optional[FilterLookup[datetime]] = strawberry.UNSET
    warehouse: Optional[FilterLookup[strawberry.relay.GlobalID]] = strawberry.UNSET
    client: Optional[FilterLookup[strawberry.relay.GlobalID]] = strawberry.UNSET
    description: Optional[str] = strawberry.UNSET
