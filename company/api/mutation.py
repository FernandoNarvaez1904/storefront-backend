from strawberry_django_plus import gql

from company.api.types.paymeny_method_type.payment_method_input import PaymentMethodCreateInput
from company.api.types.paymeny_method_type.payment_method_type import PaymentMethodType


@gql.type
class Mutation:
    payment_method_create: PaymentMethodType = gql.django.create_mutation(PaymentMethodCreateInput)
