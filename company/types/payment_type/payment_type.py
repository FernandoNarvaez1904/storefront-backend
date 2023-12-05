import decimal
from abc import ABC
from datetime import datetime

import strawberry
from strawberry.relay import Node

from company.models import Payment
from company.types.paymeny_method_type.payment_method_type import PaymentMethodType


@strawberry.django.type(Payment)
class PaymentType(Node, ABC):
    creation_date: datetime
    payment_method: PaymentMethodType
    amount: decimal.Decimal
