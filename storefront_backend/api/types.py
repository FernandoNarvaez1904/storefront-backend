from typing import Optional

import strawberry
from strawberry_django.filters import FilterLookup


@strawberry.input
class Filter:
    id: Optional[FilterLookup[strawberry.ID]] = strawberry.UNSET
