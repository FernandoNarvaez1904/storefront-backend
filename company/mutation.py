import strawberry
from strawberry_django import mutations, NodeInput

from company.types.paymeny_method_type.payment_method_input import PaymentMethodCreateInput, \
    PaymentMethodUpdateInput
from company.types.paymeny_method_type.payment_method_type import PaymentMethodType


@strawberry.type
class Mutation:
    payment_method_create: PaymentMethodType = mutations.create(PaymentMethodCreateInput)
    payment_method_update: PaymentMethodType = mutations.update(PaymentMethodUpdateInput)
    payment_method_delete: PaymentMethodType = mutations.delete(NodeInput,
                                                                          description="It is only possible to delete PaymentMethods that has no Payment referenced")
