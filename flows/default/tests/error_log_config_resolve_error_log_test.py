# flows/default/tests/error_log_config_resolve_error_log_test.py
"""
    #TODO add comment
"""
import json
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.error_log import ErrorLogBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.error_log_config_resolve_error_log import FlowErrorLogConfigResolveErrorLog, FlowErrorLogConfigResolveErrorLogResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.error_log import ErrorLogFactory
class TestErrorLogConfigResolveErrorLogPostModelResponse:
    """
    #TODO add comment
    """
    def test_flow_error_log_config_resolve_error_log_result_to_json(self):
        """
            #TODO add comment
        """
        # Create an instance and set attributes
        result = FlowErrorLogConfigResolveErrorLogResult()
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
        flow = FlowErrorLogConfigResolveErrorLog(session_context)
        error_log = await ErrorLogFactory.create_async(session)
        error_log_bus_obj = ErrorLogBusObj(session_context)
        await error_log_bus_obj.load_from_obj_instance(error_log)
        role_required = "Config"

# endset
        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    error_log_bus_obj,

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
                    error_log_bus_obj,

# endset  # noqa: E122
                )
        session_context.role_name_csv = role_required
        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     error_log_code=error_log.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowErrorLogConfigResolveErrorLogResult)

