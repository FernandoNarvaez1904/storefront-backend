from strawberry import Schema

from storefront_backend.api.mutation import Mutation
from storefront_backend.api.query import Query

schema = Schema(query=Query, mutation=Mutation, )
