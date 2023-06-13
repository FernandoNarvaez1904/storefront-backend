from strawberry_django_plus import gql

from sales.models import SaleDocument


@gql.field
async def total_sales_amount() -> float:
    sales = SaleDocument.objects.filter()
    return sum([sale.total async for sale in sales])
