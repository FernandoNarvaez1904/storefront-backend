from typing import Optional, Any

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.handlers.asgi import ASGIRequest
from django.test import AsyncRequestFactory  # type: ignore
from graphql import GraphQLResolveInfo, OperationDefinitionNode, GraphQLSchema
from graphql.pyutils import Path
from strawberry.django.context import StrawberryDjangoContext
from strawberry.django.views import TemporalHttpResponse
from strawberry.field import StrawberryField
from strawberry.types import Info

from storefront_backend.api.schema import schema
from users.models import User


async def get_async_request_with_user_and_session(user: Optional[User] = None) -> ASGIRequest:
    request = AsyncRequestFactory().post("/graphql")
    middleware = SessionMiddleware(lambda x: x)
    middleware.process_request(request)

    if user:
        request.user = user
    else:
        request.user = AnonymousUser()

    return request


async def create_user_with_permission(username: str, password: str, permission_codename: str = "") -> User:
    user: User = await User.objects.acreate(username=username, password=password)

    if permission_codename:
        perm = await Permission.objects.aget(codename=permission_codename)
        await sync_to_async(user.user_permissions.add)(perm)

    return user


def get_info(field: StrawberryField, field_name: str, return_type: Any,
             parent_type: Any) -> Info:
    # Faking Request
    async_request = AsyncRequestFactory().post("/graphql")
    middleware = SessionMiddleware(lambda x: x)
    middleware.process_request(async_request)

    def is_awaitable(a):
        return False

    # Faking Info for resolver
    resolver_info = GraphQLResolveInfo(
        context=StrawberryDjangoContext(async_request, TemporalHttpResponse()),
        root_value=None,
        variable_values={},
        fragments={},
        field_name=field_name,
        operation=OperationDefinitionNode(),
        field_nodes=[],
        is_awaitable=is_awaitable,
        return_type=schema.schema_converter.from_object(return_type._type_definition),
        parent_type=schema.schema_converter.from_object(parent_type._type_definition),
        schema=GraphQLSchema(),
        path=Path("", "", "")
    )
    return Info(_raw_info=resolver_info, _field=field)
