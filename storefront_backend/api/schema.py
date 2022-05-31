from strawberry import Schema

from inventory.api.types.item import not_in_schema_types as inventory_not_in_schema_types
from storefront_backend.api.mutation import Mutation
from storefront_backend.api.query import Query

schema = Schema(query=Query, mutation=Mutation, types=[*inventory_not_in_schema_types])
