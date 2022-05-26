from strawberry import Schema

from inventory.api.types.product.user_error_types import SKUNotUniqueError, BarcodeNotUniqueError
from storefront_backend.api.mutation import Mutation
from storefront_backend.api.query import Query

schema = Schema(query=Query, mutation=Mutation, types=[SKUNotUniqueError, BarcodeNotUniqueError])
