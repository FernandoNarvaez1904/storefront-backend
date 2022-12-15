from django.test import TestCase
from strawberry import UNSET
from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from storefront_backend.api.types import Filter
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_lookup, get_filter_arg_from_filter_input


class TestFilterArgFromLookup(TestCase):

    async def test_get_filter_arg_from_lookup(self) -> None:
        lookup = FilterLookup(starts_with="10", gt=5)
        expected_result = await get_filter_arg_from_lookup(lookup=lookup)
        self.assertDictEqual(expected_result, {"starts_with": "10", "gt": 5})

    async def test_get_filter_arg_from_lookup_exact(self) -> None:
        exact_lookup = FilterLookup(exact="hey", starts_with="10")
        expected_result = await get_filter_arg_from_lookup(lookup=exact_lookup)
        self.assertDictEqual(expected_result, {"exact": "hey", "starts_with": "10"})

    async def test_get_filter_arg_from_lookup_prefix(self) -> None:
        lookup = FilterLookup(starts_with="10")
        expected_result = await get_filter_arg_from_lookup(lookup=lookup, prefix="name")
        self.assertDictEqual(expected_result, {"name__startswith": "10"})


@gql.input
class TestFilter(Filter):
    test_str: str
    test_int: int
    test_float: float
    test_lookup_str: FilterLookup[str]


@gql.input
class AnotherFilter(Filter):
    test_str: str


@gql.input
class SomeFilter(Filter):
    another_filter: AnotherFilter


class TestGetArgFromFilterInput(TestCase):
    async def test_get_arg_from_filter_input_empty_unset(self) -> None:
        # Test all values in filter UNSET
        all_unset_filter = TestFilter(
            test_str=UNSET,
            test_int=UNSET,
            test_float=UNSET,
            id=UNSET,
            test_lookup_str=UNSET
        )
        empty_dict = await get_filter_arg_from_filter_input(filter=all_unset_filter)
        self.assertDictEqual(empty_dict, {})

    async def test_get_arg_from_filter_input_simple_exclusive_values(self) -> None:
        # Test Simple exclusive values
        exclusive_values_filter = TestFilter(
            test_str="hello",
            test_int=23,
            test_float=23.5,
            id=UNSET,
            test_lookup_str=UNSET
        )
        exclusive_values = await get_filter_arg_from_filter_input(filter=exclusive_values_filter)
        self.assertDictEqual(exclusive_values, {
            "test_str": "hello",
            "test_int": 23,
            "test_float": 23.5,
        })

    async def test_get_arg_from_filter_input_lookup_values(self) -> None:
        # Test lookup values
        lookup_values_filter = TestFilter(
            test_str=UNSET,
            test_int=UNSET,
            test_float=UNSET,
            id=UNSET,
            test_lookup_str=FilterLookup(exact="45")
        )
        exclusive_values_lookup = await get_filter_arg_from_filter_input(filter=lookup_values_filter)
        self.assertDictEqual(exclusive_values_lookup, {
            "test_lookup_str__exact": "45"
        })

    async def test_get_arg_from_filter_input_lookup_simple_values(self) -> None:
        # Test lookup and simple values
        lookup_values_filter = TestFilter(
            test_str=UNSET,
            test_int=UNSET,
            test_float=34,
            id=UNSET,
            test_lookup_str=FilterLookup(exact="45")
        )
        exclusive_values = await get_filter_arg_from_filter_input(filter=lookup_values_filter)
        self.assertDictEqual(exclusive_values, {
            "test_lookup_str__exact": "45",
            "test_float": 34
        })

    async def test_get_arg_from_filter_input_input_filter_inside_filter(self) -> None:
        # Test Include another Filter

        some_filter_instance = SomeFilter(
            id=UNSET,
            another_filter=AnotherFilter(
                id=UNSET,
                test_str="hello"
            )
        )
        another_filter_inside = await get_filter_arg_from_filter_input(filter=some_filter_instance)
        self.assertDictEqual({"another_filter__test_str": "hello"}, another_filter_inside)

    async def test_get_arg_from_filter_input_prefix_simple_values(self) -> None:
        # Test prefix with simple values
        prefix = "prefix"
        exclusive_values_filter = TestFilter(
            test_str="hello",
            test_int=23,
            test_float=23.5,
            id=UNSET,
            test_lookup_str=UNSET
        )
        exclusive_values = await get_filter_arg_from_filter_input(filter=exclusive_values_filter, prefix=prefix)
        self.assertDictEqual(exclusive_values, {
            f"{prefix}__test_str": "hello",
            f"{prefix}__test_int": 23,
            f"{prefix}__test_float": 23.5,
        })

    async def test_get_arg_from_filter_input_prefix_with_filter_in_filter(self) -> None:
        some_filter_instance = SomeFilter(
            id=UNSET,
            another_filter=AnotherFilter(
                id=UNSET,
                test_str="hello"
            )
        )
        prefix = "prefix"
        # Test prefix with another value inside
        another_filter_inside = await get_filter_arg_from_filter_input(filter=some_filter_instance, prefix=prefix)
        self.assertDictEqual({f"{prefix}__another_filter__test_str": "hello"}, another_filter_inside)

    async def test_get_arg_from_filter_input_prefix_with_exclusive_values(self) -> None:
        lookup_values_filter = TestFilter(
            test_str=UNSET,
            test_int=UNSET,
            test_float=34,
            id=UNSET,
            test_lookup_str=FilterLookup(exact="45")
        )
        # Test prefix with exclusive values
        prefix = "prefix"
        exclusive_values = await get_filter_arg_from_filter_input(filter=lookup_values_filter, prefix=prefix)
        self.assertDictEqual(exclusive_values, {
            f"{prefix}__test_lookup_str__exact": "45",
            f"{prefix}__test_float": 34
        })
