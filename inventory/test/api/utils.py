from typing import List

from asgiref.sync import sync_to_async
from django.test import TestCase
from graphql import ExecutionResult

from inventory.models import Item, ItemDetail


async def test_execution_result(test_case: TestCase, execution_result: ExecutionResult,
                                operation_name: str) -> ExecutionResult:
    test_case.assertIsNone(execution_result.errors)
    exec_result_data: dict = execution_result.data
    # Test data is not null
    test_case.assertIsNotNone(exec_result_data)

    data = exec_result_data.get(operation_name)
    test_case.assertIsNotNone(data)

    return execution_result


async def test_relay_connection(test_case: TestCase,
                                execution_result: ExecutionResult = None,
                                exec_result_data=None,
                                operation_name: str = "",
                                ) -> ExecutionResult | dict:
    """
        Tests all the standard fields of a connection query.

        if exec_result_data the schema and query connection parameters can be omitted,
        and the exec_result_data will be returned
    """

    connection_data = None
    if not exec_result_data:

        # Test has no execution error
        await test_execution_result(test_case, execution_result, operation_name)
        connection_data = execution_result.data.get(operation_name)
    else:
        connection_data = exec_result_data
        # This is done to make the func return a single variable in each case
        execution_result = exec_result_data

    # Test if all fields return
    test_case.assertNotIn(None, connection_data.values())

    edges = connection_data.get("edges")
    # Test if all fields return
    test_case.assertNotIn(None, edges)

    return execution_result


async def test_mutation(test_case: TestCase, execution_result: ExecutionResult,
                        operation_name: str):
    execution_result = await test_execution_result(test_case, execution_result, operation_name)

    result_data = execution_result.data.get(operation_name)
    # Test if UserError is returned
    user_errors: List = result_data.get("userErrors")
    test_case.assertIsNotNone(user_errors)

    # Test Mutation Result UserError is empty
    test_case.assertFalse(len(user_errors))

    # Test if node is returned
    node: dict = result_data.get("node")
    test_case.assertIsNotNone(node)

    # Test if all fields return
    test_case.assertNotIn(None, node.values())


async def create_bulk_of_item(num: int, active: bool = True, seed: str = "") -> List[Item]:
    item_list = []
    for i in range(num):
        item = await sync_to_async(Item.objects.create)(sku=f"{seed}{i}", is_active=active)

        await sync_to_async(ItemDetail.objects.create)(
            name=f"{seed}itemDetail{i}",
            barcode=f"{seed}890432",
            cost=10,
            markup=50,
            root_item=item,
        )
        item_list.append(item)
    return item_list


def get_connection_query(node_fragment: str, field_name: str = "", extra_args: str = "") -> str:
    return f"""
      {field_name}(
        # Args were included to test if they exist
        before: null
        after: null
        first: null
        last: null
        {extra_args}
      ){{
        edges{{
          cursor
          node{{
            {node_fragment}
          }}
        }}
        pageInfo{{
            hasNextPage
            hasPreviousPage
            startCursor
            endCursor
            __typename
        }}
        totalCount
        __typename
      }}
        """
