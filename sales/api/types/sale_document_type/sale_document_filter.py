from datetime import datetime
from typing import Optional

import strawberry
from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from storefront_backend.api.types import Filter


@gql.input
class TotalSaleSearchFilter(Filter):
    creation_date: Optional[FilterLookup[datetime]] = strawberry.UNSET
    warehouse: Optional[FilterLookup[gql.relay.GlobalID]] = strawberry.UNSET
    client: Optional[FilterLookup[gql.relay.GlobalID]] = strawberry.UNSET
    description: Optional[str] = strawberry.UNSET
