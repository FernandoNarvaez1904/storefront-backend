import decimal

import strawberry
from strawberry_django import  NodeInput

from company.models import Payment


@strawberry.django.input(Payment)
class PaymentCreateInput:
    payment_method: NodeInput
    amount: decimal.Decimal
