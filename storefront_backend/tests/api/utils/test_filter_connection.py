from django.test import TestCase
from strawberry import UNSET
from strawberry_django.filters import FilterLookup
from strawberry_django_plus import gql

from storefront_backend.api.types import Filter
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_lookup, get_filter_arg_from_filter_input


class FilterConnectionTest(TestCase):
    def setUp(self):
        pass

    async def test_get_filter_arg_from_lookup(self):
        # Test passing None as lookup returns empty dict
        empty_dict = await get_filter_arg_from_lookup(lookup=None)
        self.assertDictEqual(empty_dict, {})

        # Test exception raised when lookup does not implement FilterLookup
        class AnyClass:
            pass

        with self.assertRaises(ValueError):
            await get_filter_arg_from_lookup(
                lookup=AnyClass()
            )

        # Test lookup not prefix
        exact_lookup = FilterLookup(exact="hey", starts_with="10")
        expected_result = await get_filter_arg_from_lookup(lookup=exact_lookup)
        self.assertDictEqual(expected_result, {"exact": "hey", "starts_with": "10"})

        # Test lookup with prefix
        expected_result = await get_filter_arg_from_lookup(lookup=exact_lookup, prefix="name")
        self.assertDictEqual(expected_result, {"name__exact": "hey", "name__startswith": "10"})

    async def test_get_arg_from_filter_input(self):
        # Test passing None as lookup returns empty dict
        empty_dict = await get_filter_arg_from_filter_input(filter=None)
        self.assertDictEqual(empty_dict, {})

        # Test exception raised when filter does not implement FilterLookup
        class AnyClass:
            pass

        with self.assertRaises(ValueError):
            await get_filter_arg_from_filter_input(
                filter=AnyClass()
            )

        @gql.input
        class TestFilter(Filter):
            test_str: str
            test_int: int
            test_float: float
            test_lookup_str: FilterLookup[str]

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

        # Test Include another Filter
        @gql.input
        class AnotherFilter(Filter):
            test_str: str

        @gql.input
        class SomeFilter(Filter):
            another_filter: AnotherFilter

        some_filter_instance = SomeFilter(
            id=UNSET,
            another_filter=AnotherFilter(
                id=UNSET,
                test_str="hello"
            )
        )
        another_filter_inside = await get_filter_arg_from_filter_input(filter=some_filter_instance)
        self.assertDictEqual({"another_filter__test_str": "hello"}, another_filter_inside)

        # Test prefix with simple values
        prefix = "prefix"
        exclusive_values = await get_filter_arg_from_filter_input(filter=exclusive_values_filter, prefix=prefix)
        self.assertDictEqual(exclusive_values, {
            f"{prefix}__test_str": "hello",
            f"{prefix}__test_int": 23,
            f"{prefix}__test_float": 23.5,
        })

        # Test prefix with another value inside
        another_filter_inside = await get_filter_arg_from_filter_input(filter=some_filter_instance, prefix=prefix)
        self.assertDictEqual({f"{prefix}__another_filter__test_str": "hello"}, another_filter_inside)

        # Test prefix with exclusive values and simple values
        exclusive_values = await get_filter_arg_from_filter_input(filter=lookup_values_filter, prefix=prefix)
        self.assertDictEqual(exclusive_values, {
            f"{prefix}__test_lookup_str__exact": "45",
            f"{prefix}__test_float": 34
        })
