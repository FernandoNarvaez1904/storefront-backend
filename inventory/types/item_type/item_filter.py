from strawberry_django.filters import FilterLookup
import strawberry

from storefront_backend.api.types import Filter


@strawberry.input
class ItemFilter(Filter):
    name: FilterLookup[str]
