from typing import Optional

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.handlers.asgi import ASGIRequest
from django.test import AsyncRequestFactory  # type: ignore

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
