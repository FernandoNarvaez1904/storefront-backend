from typing import Optional

import strawberry

from storefront_backend.api.relay.connection import get_cursor_page_from_queryset, get_connection_from_cursor_page, \
    Connection
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input
from users.api.queries.user_connection.user_connection_filter import UserFilter
from users.api.types.user_type import UserType
from users.models import User


async def user_connection_resolver(
        before: Optional[strawberry.ID] = None,
        after: Optional[strawberry.ID] = None,
        first: Optional[int] = None,
        last: Optional[int] = None, filter: Optional[UserFilter] = None) -> Connection[UserType]:
    filt = {}
    if filter:
        filt = await get_filter_arg_from_filter_input(filter=filter)

    qs = User.objects.filter(**filt)
    page = await get_cursor_page_from_queryset(qs, after, before, first, last)
    connection = await get_connection_from_cursor_page(page, UserType)
    return connection
