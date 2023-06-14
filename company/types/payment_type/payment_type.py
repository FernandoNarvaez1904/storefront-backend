import decimal
from abc import ABC
from datetime import datetime

from strawberry_django_plus import gql

from company.models import Payment
from company.types.paymeny_method_type.payment_method_type import PaymentMethodType


@gql.django.type(Payment)
class PaymentType(gql.NodeType, ABC):
    creation_date: datetime
    payment_method: PaymentMethodType
    amount: decimal.Decimal
