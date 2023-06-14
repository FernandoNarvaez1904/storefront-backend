from strawberry_django_plus import gql

from company.types.paymeny_method_type.payment_method_input import PaymentMethodCreateInput, \
    PaymentMethodUpdateInput
from company.types.paymeny_method_type.payment_method_type import PaymentMethodType


@gql.type
class Mutation:
    payment_method_create: PaymentMethodType = gql.django.create_mutation(PaymentMethodCreateInput)
    payment_method_update: PaymentMethodType = gql.django.update_mutation(PaymentMethodUpdateInput)
    payment_method_delete: PaymentMethodType = gql.django.delete_mutation(gql.NodeInput,
                                                                          description="It is only possible to delete PaymentMethods that has no Payment referenced")
