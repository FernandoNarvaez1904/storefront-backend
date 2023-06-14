from strawberry_django_plus import gql

from sales.mutations.sale_document_mutations import sale_document_create
from sales.types.client_type.client_input import ClientCreateInput, ClientUpdateInput
from sales.types.client_type.client_type import ClientType


@gql.type
class Mutation:
    client_create: ClientType = gql.django.create_mutation(ClientCreateInput)
    client_update: ClientType = gql.django.update_mutation(ClientUpdateInput)
    client_delete: ClientType = gql.django.delete_mutation(gql.NodeInput,
                                                           description="Client instances can only be deleted when there is no "
                                                                       "reference to any Document")

    sale_document_create = sale_document_create
