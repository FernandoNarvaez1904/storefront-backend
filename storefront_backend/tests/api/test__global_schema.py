from django.test import TestCase

from storefront_backend.api.schema import schema


class SchemaTestCase(TestCase):

    def setUp(self):
        self.introspection = schema.introspect()

    def test_can_introspect(self):
        self.assertIn("__schema", self.introspection)

    def test_has_query(self):
        __schema = self.introspection.get("__schema")
        self.assertIsNotNone(__schema.get("queryType"))

    def test_has_mutation(self):
        __schema = self.introspection.get("__schema")
        self.assertIsNotNone(__schema.get("mutationType"))
