from strawberry import Schema
from strawberry.extensions import ParserCache, ValidationCache
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from inventory.api.types.item import not_in_schema_types as inventory_not_in_schema_types
from storefront_backend.api.mutation import Mutation
from storefront_backend.api.query import Query

schema = Schema(query=Query, mutation=Mutation, types=[*inventory_not_in_schema_types],
                extensions=[ParserCache(), ValidationCache(), DjangoOptimizerExtension()])
