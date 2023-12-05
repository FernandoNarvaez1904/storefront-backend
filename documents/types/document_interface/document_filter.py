from datetime import datetime

from strawberry_django.filters import FilterLookup
import strawberry

from inventory.types.warehouse_type.warehouse_filter import WarehouseFilter
from storefront_backend.api.types import Filter


@strawberry.input
class DocumentFilter(Filter):
    creation_date: FilterLookup[datetime]
    modification_date: FilterLookup[datetime]
    description: FilterLookup[str]
    warehouse: WarehouseFilter
