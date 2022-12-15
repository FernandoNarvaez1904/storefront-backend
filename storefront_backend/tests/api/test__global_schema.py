from typing import cast, Any

from django.test import TestCase

from storefront_backend.api.schema import schema


class SchemaTestCase(TestCase):

    def setUp(self) -> None:
        self.introspection = schema.introspect()

    def test_can_introspect(self) -> None:
        self.assertIn("__schema", self.introspection)

    def test_has_query(self) -> None:
        __schema = cast(dict[str, dict[str, Any]], self.introspection.get("__schema"))
        self.assertIsNotNone(__schema.get("queryType"))

    def test_has_mutation(self) -> None:
        __schema = cast(dict[str, dict[str, Any]], self.introspection.get("__schema"))
        self.assertIsNotNone(__schema.get("mutationType"))
