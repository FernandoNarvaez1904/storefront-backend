import decimal

from strawberry_django_plus import gql

from company.models import Payment


@gql.django.input(Payment)
class PaymentCreateInput:
    payment_method: gql.NodeInput
    amount: decimal.Decimal
