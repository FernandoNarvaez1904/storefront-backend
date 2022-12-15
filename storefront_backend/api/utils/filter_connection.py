from typing import TypeVar, List

from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from strawberry_django.filters import FilterLookup, lookup_name_conversion_map

from storefront_backend.api.types import Filter

FilterInput = TypeVar("FilterInput")


async def get_filter_arg_from_lookup(lookup: FilterLookup, prefix: str = "") -> dict:
    result = {}

    for name, val in lookup.__dict__.items():
        if val:
            if prefix:
                if name in lookup_name_conversion_map.keys():
                    name = f"__{lookup_name_conversion_map[name]}"
                else:
                    name = f"__{name}"
            result.update({f"{prefix}{name}": val})

    return result


async def get_filter_arg_from_filter_input(filter: FilterInput, prefix: str = "") -> dict:
    filter_result = {}

    for name, value in filter.__dict__.items():

        if not value:
            continue

        if prefix:
            name = f"{prefix}__{name}"

        value_is_another_filter = isinstance(value, Filter)
        if value_is_another_filter:
            result = await get_filter_arg_from_filter_input(prefix=name, filter=value)
            filter_result.update(result)
            continue

        value_is_lookup = isinstance(value, FilterLookup)
        if value_is_lookup:
            result = await get_filter_arg_from_lookup(lookup=value, prefix=name)
            filter_result.update(result)
            continue

        # If value is a simple exact filter
        filter_result.update({f"{name}": value})

    return filter_result


async def get_lazy_query_set_as_list(query_set: QuerySet) -> List:
    list_coroutine = sync_to_async(len)
    return await list_coroutine(query_set)
