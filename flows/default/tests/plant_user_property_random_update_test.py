# flows/default/tests/plant_user_property_random_update_test.py
# pylint: disable=unused-import

"""
This module contains unit tests for the
`FlowPlantUserPropertyRandomUpdateResult` and
`FlowPlantUserPropertyRandomUpdate` classes.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.plant_user_property_random_update import (
    FlowPlantUserPropertyRandomUpdate,
    FlowPlantUserPropertyRandomUpdateResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.plant import (
    PlantFactory)


class TestPlantUserPropertyRandomUpdatePostModelResponse:
    """
    This class contains unit tests for the
    `FlowPlantUserPropertyRandomUpdateResult` class.
    """

    def test_flow_result_to_json(self):
        """
        Test the `to_json` method of the
        `FlowPlantUserPropertyRandomUpdateResult` class.
        """

        # Create an instance and set attributes
        result = FlowPlantUserPropertyRandomUpdateResult()
        result.context_object_code = uuid.uuid4()


        # Call to_json method
        json_output = result.to_json()

        # Parse JSON output
        data = json.loads(json_output)

        # Assert individual fields
        assert data["context_object_code"] == (
            str(result.context_object_code))


    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        Test the `process` method of the
        `FlowPlantUserPropertyRandomUpdate` class.
        """

        session_context = SessionContext(dict(), session)
        flow = FlowPlantUserPropertyRandomUpdate(
            session_context)

        plant = await \
            PlantFactory.create_async(
                session)

        plant_bus_obj = PlantBusObj(session_context)
        plant_bus_obj.load_from_obj_instance(plant)

        role_required = "User"


        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                await flow.process(
                    plant_bus_obj,

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
                    plant_bus_obj,

# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required

        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     plant_code=plant.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowPlantUserPropertyRandomUpdateResult)
