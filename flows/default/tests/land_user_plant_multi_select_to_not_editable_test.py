# flows/default/tests/land_user_plant_multi_select_to_not_editable_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`FlowLandUserPlantMultiSelectToNotEditableResult` and
`FlowLandUserPlantMultiSelectToNotEditable` classes.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_user_plant_multi_select_to_not_editable import (
    FlowLandUserPlantMultiSelectToNotEditable,
    FlowLandUserPlantMultiSelectToNotEditableResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.land import (
    LandFactory)


class TestLandUserPlantMultiSelectToNotEditablePostModelResponse:
    """
    This class contains unit tests for the
    `FlowLandUserPlantMultiSelectToNotEditableResult` class.
    """

    def test_flow_result_to_json(self):
        """
        Test the `to_json` method of the
        `FlowLandUserPlantMultiSelectToNotEditableResult` class.
        """

        # Create an instance and set attributes
        result = FlowLandUserPlantMultiSelectToNotEditableResult()
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
        `FlowLandUserPlantMultiSelectToNotEditable` class.
        """

        session_context = SessionContext({}, session)
        flow = FlowLandUserPlantMultiSelectToNotEditable(
            session_context)

        land = await \
            LandFactory.create_async(
                session)

        land_bus_obj = LandBusObj(session_context)
        land_bus_obj.load_from_obj_instance(land)

        role_required = "User"
        plant_code_list_csv: str = ""
        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                await flow.process(
                    land_bus_obj,
                    plant_code_list_csv,
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
                    land_bus_obj,
                    plant_code_list_csv,
# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required
