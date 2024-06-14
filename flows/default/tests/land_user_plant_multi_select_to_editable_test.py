# flows/default/tests/land_user_plant_multi_select_to_editable_test.py
"""
    #TODO add comment
"""
import asyncio
from decimal import Decimal
import json
import uuid
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_user_plant_multi_select_to_editable import FlowLandUserPlantMultiSelectToEditable, FlowLandUserPlantMultiSelectToEditableResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.land import LandFactory
from models import Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants
class TestLandUserPlantMultiSelectToEditablePostModelResponse:
    """
    #TODO add comment
    """
    def test_flow_land_user_plant_multi_select_to_editable_result_to_json(self):
        # Create an instance and set attributes
        result = FlowLandUserPlantMultiSelectToEditableResult()
        result.context_object_code = uuid.uuid4()

# endset
        # Call to_json method
        json_output = result.to_json()
        # Parse JSON output
        data = json.loads(json_output)
        # Assert individual fields
        assert data["context_object_code"] == str(result.context_object_code)

# endset
    #todo finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        session_context = SessionContext(dict(), session)
        flow = FlowLandUserPlantMultiSelectToEditable(session_context)
        land = await LandFactory.create_async(session)
        land_bus_obj = LandBusObj(session_context)
        await land_bus_obj.load_from_obj_instance(land)
        role_required = "User"
        plant_code_list_csv: str = "",
# endset
        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    land_bus_obj,
                    plant_code_list_csv,
# endset
                )
        session_context.role_name_csv = role_required
        customerCodeMatchRequired = False
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if customerCodeMatchRequired is True:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    land_bus_obj,
                    plant_code_list_csv,
# endset
                )
        session_context.role_name_csv = role_required
        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     land_code=land.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowLandUserPlantMultiSelectToEditableResult)

