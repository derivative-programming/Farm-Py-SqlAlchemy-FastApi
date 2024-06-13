# flows/default/tests/plant_user_property_random_update_test.py
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
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.plant_user_property_random_update import FlowPlantUserPropertyRandomUpdate, FlowPlantUserPropertyRandomUpdateResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.plant import PlantFactory
from models import Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants
class TestPlantUserPropertyRandomUpdatePostModelResponse:
    """
    #TODO add comment
    """
    def test_flow_plant_user_property_random_update_result_to_json(self):
        # Create an instance and set attributes
        result = FlowPlantUserPropertyRandomUpdateResult()
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
        flow = FlowPlantUserPropertyRandomUpdate(session_context)
        plant = await PlantFactory.create_async(session)
        plant_bus_obj = PlantBusObj(session_context)
        await plant_bus_obj.load(plant_obj_instance=plant)
        role_required = "User"

# endset
        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    plant_bus_obj,

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
                    plant_bus_obj,

# endset
                )
        session_context.role_name_csv = role_required
        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     plant_code=plant.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowPlantUserPropertyRandomUpdateResult)

