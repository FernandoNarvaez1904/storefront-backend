from strawberry import Schema
from strawberry.extensions import ValidationCache, ParserCache
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from storefront_backend.api.mutation import Mutation
from storefront_backend.api.query import Query

schema = Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, ValidationCache(), ParserCache()])
