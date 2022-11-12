from typing import List

from asgiref.sync import async_to_sync
from django.test import TransactionTestCase
from strawberry_django.filters import FilterLookup

from inventory.api.queries.item_connection.item_connection_filter import ItemFilter
from inventory.api.queries.item_connection.item_connection_resolver import item_connection_resolver
from inventory.api.types.item import ItemType
from inventory.models import Item
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.connection import Connection


class ItemConnectionResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        self.item_number = 20
        temp: List[Item] = async_to_sync(create_bulk_of_item)(self.item_number)

    async def test_item_connection_resolver_response(self):
        response: Connection[ItemType] = await item_connection_resolver()

        # Test if response is correct type
        self.assertIsInstance(response, Connection)

        # Test if all avaible items returned
        self.assertEqual(self.item_number, response.total_count)

        # Test if total_count works
        self.assertEqual(response.total_count, len(response.edges))

    async def test_item_connection_resolver_filter_response(self):
        filter = ItemFilter(name=FilterLookup(contains="1"))
        response: Connection[ItemType] = await item_connection_resolver(filter=filter)

        # Test if response is correct type
        self.assertIsInstance(response, Connection)

        # Test is the total of items is the same as created
        self.assertEqual(self.item_number, response.total_count)

        # Test if only filtered items were returned
        self.assertNotEqual(response.total_count, len(response.edges))
        self.assertEqual(11, len(response.edges))
        # Test if edge_count is correct
        self.assertEqual(11, response.page_info.edges_count)
