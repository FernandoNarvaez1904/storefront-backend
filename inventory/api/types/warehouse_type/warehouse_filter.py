from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from storefront_backend.api.types import Filter


@gql.input
class WarehouseFilter(Filter):
    name: FilterLookup[str]
