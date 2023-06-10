from datetime import datetime

from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from inventory.api.types.warehouse_type.warehouse_filter import WarehouseFilter
from storefront_backend.api.types import Filter


@gql.input
class DocumentFilter(Filter):
    creation_date: FilterLookup[datetime]
    modification_date: FilterLookup[datetime]
    description: FilterLookup[str]
    warehouse: WarehouseFilter
