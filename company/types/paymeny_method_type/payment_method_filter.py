from typing import Optional

import strawberry
from strawberry_django.filters import FilterLookup
import strawberry

from storefront_backend.api.types import Filter


@strawberry.input
class PaymentMethodFilter(Filter):
    name: Optional[FilterLookup[str]] = strawberry.UNSET
