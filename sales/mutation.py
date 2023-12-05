import strawberry
from strawberry_django import  NodeInput, mutations


from sales.mutations.sale_document_mutations import sale_document_create
from sales.types.client_type.client_input import ClientCreateInput, ClientUpdateInput
from sales.types.client_type.client_type import ClientType
from sales.types.sale_document_type.sale_document_type import SaleDocumentType

@strawberry.type
class Mutation:
    client_create: ClientType = mutations.create(ClientCreateInput)
    client_update: ClientType = mutations.update(ClientUpdateInput)
    client_delete: ClientType = mutations.delete(NodeInput,
                                                           description="Client instances can only be deleted when there is no "
                                                                       "reference to any Document")

    sale_document_create = sale_document_create
    sale_document_delete: SaleDocumentType = mutations.delete(NodeInput)
