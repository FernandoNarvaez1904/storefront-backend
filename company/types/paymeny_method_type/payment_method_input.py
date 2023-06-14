from typing import Optional

from strawberry_django_plus import gql

from company.models import PaymentMethod


@gql.django.input(PaymentMethod)
class PaymentMethodCreateInput:
    name: str


@gql.django.input(PaymentMethod)
class PaymentMethodUpdateInput(gql.NodeInput):
    name: Optional[str]
