from datetime import datetime

from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from storefront_backend.api.types import Filter


@gql.input
class UserFilter(Filter):
    user_name: FilterLookup[str]
    first_name: FilterLookup[str]
    last_name: FilterLookup[str]
    email: FilterLookup[str]
    is_staff: FilterLookup[bool]
    is_activate: FilterLookup[bool]
    date_joined: FilterLookup[datetime]
