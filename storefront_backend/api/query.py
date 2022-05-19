from strawberry_django_plus import gql


@gql.type
class Query:

    @gql.field
    def placeholder(self) -> str:
        return "placeholder"
