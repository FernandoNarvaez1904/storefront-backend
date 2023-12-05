from datetime import datetime

from strawberry_django.filters import FilterLookup
import strawberry

from storefront_backend.api.types import Filter


@strawberry.input
class UserFilter(Filter):
    user_name: FilterLookup[str]
    first_name: FilterLookup[str]
    last_name: FilterLookup[str]
    email: FilterLookup[str]
    is_staff: FilterLookup[bool]
    is_activate: FilterLookup[bool]
    date_joined: FilterLookup[datetime]
