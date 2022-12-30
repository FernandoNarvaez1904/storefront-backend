from typing import List, Optional

import strawberry
from django.test import TestCase

from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.relay.node import Node
from storefront_backend.api.types import InputTypeInterface, UserError


@strawberry.type
class PayloadType(PayloadTypeInterface):
    user_errors: List[UserError]
    node: Optional[Node]


@strawberry.type
class NodeIns(Node):
    id: strawberry.ID


@strawberry.type
class InputType(InputTypeInterface):
    pass


class GqlMutationPayloadTest(TestCase):
    def setUp(self) -> None:
        self.input_type = InputType
        self.payload_type = PayloadType
        self.payload_type_ins = PayloadType(user_errors=[], node=NodeIns(id=Node.encode_id("1")))

        self.node = NodeIns

    async def _n_test_gql_mutation_payload(self) -> None:
        # If all mutations are working and its test passing this can work
        # I could not figure how to test it in isolation. solo the mutation working
        # is good enough

        # Leaving this function here JIC
        pass
