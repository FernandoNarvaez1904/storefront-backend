from strawberry import Schema


from inventory.api.types.exported_types import exported_types as inventory_not_in_schema_types
from storefront_backend.api.mutation import Mutation
from storefront_backend.api.query import Query
from users.api.types.exported_types import exported_types as users_not_in_schema_types

schema = Schema(query=Query, mutation=Mutation, types=[*inventory_not_in_schema_types, *users_not_in_schema_types])
