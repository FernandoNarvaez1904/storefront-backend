from strawberry_django_plus import gql

from documents.types.document_interface.document_filter import DocumentFilter


@gql.input
class StockRecountDocumentFilter(DocumentFilter):
    pass
