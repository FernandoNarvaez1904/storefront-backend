from typing import Optional

from strawberry_django_plus import gql


@gql.type
class Query:
    node: Optional[gql.Node] = gql.django.node()
