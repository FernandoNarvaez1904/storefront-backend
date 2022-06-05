from abc import ABC
from typing import List, Optional

from django.test import TestCase
from strawberry_django_plus import gql

from storefront_backend.api.types import InputTypeInterface, PayloadTypeInterface, UserError
from storefront_backend.api.utils.gql_mutation_payload import check_if_type_vars_are_correct_instance
from users.models import User


class GqlMutationPayloadTest(TestCase):
    def setUp(self):
        @gql.type
        class InputType(InputTypeInterface):
            pass

        self.input_type = InputType

        @gql.type
        class PayloadType(PayloadTypeInterface):
            user_errors: List[UserError]
            node: Optional[gql.Node]

        @gql.django.type(User)
        class NodeIns(gql.Node, ABC):
            id: gql.relay.GlobalID

        self.payload_type = PayloadType
        self.payload_type_ins = PayloadType(user_errors=[], node=NodeIns())

        self.node = NodeIns

    async def test_check_if_type_vars_are_correct_instance(self):
        correct_inputs = {
            "input_type": self.input_type,
            "payload_type": self.payload_type,
            "returned_type": self.node
        }
        # Test no errors
        self.assertTrue(await check_if_type_vars_are_correct_instance(**correct_inputs))

        class AnotherClass:
            pass

        # Test Input None or another class
        with self.assertRaises(TypeError) as e:
            input_bad = {**correct_inputs, "input_type": None}
            await check_if_type_vars_are_correct_instance(**input_bad)
            input_bad = {**correct_inputs, "input_type": AnotherClass()}
            await check_if_type_vars_are_correct_instance(**input_bad)

        # Test Payload None or another class
        with self.assertRaises(TypeError) as e:
            input_bad = {**correct_inputs, "payload_type": None}
            await check_if_type_vars_are_correct_instance(**input_bad)
            input_bad = {**correct_inputs, "payload_type": AnotherClass()}
            await check_if_type_vars_are_correct_instance(**input_bad)

        # Test Returned None or another class
        with self.assertRaises(TypeError) as e:
            input_bad = {**correct_inputs, "returned_type": None}
            await check_if_type_vars_are_correct_instance(**input_bad)
            input_bad = {**correct_inputs, "returned_type": AnotherClass()}
            await check_if_type_vars_are_correct_instance(**input_bad)

        # Test  confused returned with payload
        with self.assertRaises(TypeError) as e:
            input_bad = {**correct_inputs, "returned_type": correct_inputs.get("payload_type")}
            await check_if_type_vars_are_correct_instance(**input_bad)

        # Test  confused payload with returned
        with self.assertRaises(TypeError) as e:
            input_bad = {**correct_inputs, "payload_type": correct_inputs.get("returned_type")}
            await check_if_type_vars_are_correct_instance(**input_bad)

    async def _n_test_gql_mutation_payload(self):
        # If all mutations are working and its test passing this can work
        # I could not figure how to test it in isolation. solo the mutation working
        # is good enough

        # Leaving this function here JIC
        pass

