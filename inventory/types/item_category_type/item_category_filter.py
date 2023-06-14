from typing import Optional

import strawberry
from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from storefront_backend.api.types import Filter


@gql.input
class ItemCategoryFilter(Filter):
    name: Optional[FilterLookup[str]] = strawberry.UNSET
    parent: Optional["ItemCategoryFilter"] = strawberry.UNSET
