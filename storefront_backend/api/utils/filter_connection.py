from typing import Optional, Iterable, TypeVar

from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from storefront_backend.api.types import Filter

FilterInput = TypeVar("FilterInput")


async def get_filter_arg_from_lookup(lookup: FilterLookup, prefix: str = "") -> dict:
    result = {}

    if lookup:
        if not isinstance(lookup, FilterLookup):
            raise ValueError(f"{lookup.__class__.__name__} is not implementing {FilterLookup.__name__}")

        for name, val in lookup.__dict__.items():
            if val:
                if prefix:
                    name = f"__{name}"
                result.update({f"{prefix}{name}": val})

    return result


async def get_filter_arg_from_filter_input(filter: Optional[FilterInput], prefix: str = "") -> dict:
    filter_result = {}

    if filter:

        if not isinstance(filter, Filter):
            raise ValueError(f"{filter.__class__.__name__} is not implementing {Filter.__name__} ")

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


def filter_connection(return_type, filter_input: FilterInput = None):
    @gql.connection
    async def wrapper(self, filter: Optional[filter_input] = None) -> Iterable[return_type]:
        filter_result = await get_filter_arg_from_filter_input(filter)
        result = return_type._django_type.model.objects.filter(**filter_result)
        return result

    return wrapper
