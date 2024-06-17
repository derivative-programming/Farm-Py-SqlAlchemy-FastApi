# flows/default/tests/plant_user_delete_test.py
"""
    #TODO add comment
"""
import json
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.plant_user_delete import FlowPlantUserDelete, FlowPlantUserDeleteResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.plant import PlantFactory
class TestPlantUserDeletePostModelResponse:
    """
    #TODO add comment
    """
    def test_flow_plant_user_delete_result_to_json(self):
        """
            #TODO add comment
        """
        # Create an instance and set attributes
        result = FlowPlantUserDeleteResult()
        result.context_object_code = uuid.uuid4()

# endset
        # Call to_json method
        json_output = result.to_json()
        # Parse JSON output
        data = json.loads(json_output)
        # Assert individual fields
        assert data["context_object_code"] == str(result.context_object_code)

# endsets
    #TODO finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = FlowPlantUserDelete(session_context)
        plant = await PlantFactory.create_async(session)
        plant_bus_obj = PlantBusObj(session_context)
        await plant_bus_obj.load_from_obj_instance(plant)
        role_required = "User"

# endset
        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    plant_bus_obj,

# endset  # noqa: E122
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

# endset  # noqa: E122
                )
        session_context.role_name_csv = role_required
        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     plant_code=plant.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowPlantUserDeleteResult)

