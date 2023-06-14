from typing import Optional

import strawberry
from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql


@strawberry.input
class Filter:
    id: Optional[FilterLookup[gql.relay.GlobalID]] = strawberry.UNSET
