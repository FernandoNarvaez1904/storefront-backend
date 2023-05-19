from typing import Optional

import strawberry
from strawberry_django.filters import FilterLookup

from storefront_backend.api.types import Filter


@strawberry.input
class UserFilter(Filter):
    username: Optional[FilterLookup[str]] = strawberry.UNSET
    first_name: Optional[FilterLookup[str]] = strawberry.UNSET
    last_name: Optional[FilterLookup[str]] = strawberry.UNSET
    email: Optional[FilterLookup[str]] = strawberry.UNSET
    is_superuser: Optional[bool] = strawberry.UNSET
    is_staff: Optional[bool] = strawberry.UNSET
    is_active: Optional[bool] = strawberry.UNSET
