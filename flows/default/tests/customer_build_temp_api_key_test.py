# flows/default/tests/customer_build_temp_api_key_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`FlowCustomerBuildTempApiKeyResult` and
`FlowCustomerBuildTempApiKey` classes.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.customer_build_temp_api_key import (
    FlowCustomerBuildTempApiKey,
    FlowCustomerBuildTempApiKeyResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.customer import (
    CustomerFactory)


class TestCustomerBuildTempApiKeyPostModelResponse:
    """
    This class contains unit tests for the
    `FlowCustomerBuildTempApiKeyResult` class.
    """

    def test_flow_result_to_json(self):
        """
        Test the `to_json` method of the
        `FlowCustomerBuildTempApiKeyResult` class.
        """

        # Create an instance and set attributes
        result = FlowCustomerBuildTempApiKeyResult()
        result.context_object_code = uuid.uuid4()
        result.tmp_org_api_key_code = uuid.uuid4()
        # Call to_json method
        json_output = result.to_json()

        # Parse JSON output
        data = json.loads(json_output)

        # Assert individual fields
        assert data["context_object_code"] == (
            str(result.context_object_code))
        assert data["tmp_org_api_key_code"] == (
            str(result.tmp_org_api_key_code))

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        Test the `process` method of the
        `FlowCustomerBuildTempApiKey` class.
        """

        session_context = SessionContext({}, session)
        flow = FlowCustomerBuildTempApiKey(
            session_context)

        customer = await \
            CustomerFactory.create_async(
                session)

        customer_bus_obj = CustomerBusObj(session_context)
        customer_bus_obj.load_from_obj_instance(customer)

        role_required = ""

        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                await flow.process(
                    customer_bus_obj,

# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required

        customer_code_match_required = False
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORGANIZATION_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORG_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True

        if customer_code_match_required is True:
            with pytest.raises(FlowValidationError):

                await flow.process(
                    customer_bus_obj,

# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required
