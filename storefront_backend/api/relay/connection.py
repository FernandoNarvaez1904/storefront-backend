from typing import TypeVar, Generic, Optional, List, Type, cast

import strawberry
from asgiref.sync import sync_to_async
from cursor_pagination import CursorPaginator, CursorPage
from django.db.models import QuerySet
from strawberry import ID

GenericType = TypeVar("GenericType")


@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination

    Instead of classic offset pagination via `page` and `limit` parameters,
    here we have a cursor of the last object and we fetch items starting from that one
    """
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]
    total_count: Optional[int]
    edges_count: Optional[int]


@strawberry.type
class Edge(Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case"""
    node: GenericType
    cursor: str


@strawberry.type
class Connection(Generic[GenericType]):
    """Represents a paginated relationship between two entities

    This pattern is used when the relationship itself has attributes.
    In a Facebook-based domain example, a friendship between two people
    would be a connection that might have a `friendshipStartTime`
    """
    page_info: PageInfo
    edges: List[Edge[GenericType]]
    total_count: int


from .node import Node

T = TypeVar("T", bound=Node)


async def get_cursor_page_from_queryset(qs: QuerySet, before: Optional[ID] = None, after: Optional[ID] = None,
                                        first: Optional[int] = None, last: Optional[int] = None) -> CursorPage:
    paginator: CursorPaginator = CursorPaginator(qs, ordering=tuple())
    if after:
        after_id = Node.decode_id(after).get("instance_id")
        after = paginator.encode_cursor([after_id])
    if before:
        before_id = Node.decode_id(before).get("instance_id")
        before = paginator.encode_cursor([before_id])
    page: CursorPage = await sync_to_async(paginator.page)(first=first, after=after, before=before, last=last)
    return page


async def get_connection_from_cursor_page(page, node: Type[T]) -> Connection[T]:
    edges: List[Edge] = []
    edges_count = await sync_to_async(len)(page)
    for item in page:
        node = cast(Type[T], node.from_model_instance(item))
        edges.append(Edge(node=node, cursor=node.id))
    page_info = PageInfo(
        has_next_page=page.has_next,
        has_previous_page=page.has_previous,
        start_cursor=edges[0].node.id if edges else None,
        end_cursor=edges[-1].node.id if edges else None,
        edges_count=edges_count,
        total_count=await node._model_.objects.acount()
    )
    connection = Connection(page_info=page_info, edges=edges, total_count=await node._model_.objects.acount()
                            )
    return connection
