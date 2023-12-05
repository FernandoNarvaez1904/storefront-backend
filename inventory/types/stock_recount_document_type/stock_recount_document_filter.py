import strawberry

from documents.types.document_interface.document_filter import DocumentFilter


@strawberry.input
class StockRecountDocumentFilter(DocumentFilter):
    pass
