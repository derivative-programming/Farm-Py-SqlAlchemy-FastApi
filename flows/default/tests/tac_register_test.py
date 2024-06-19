# flows/default/tests/tac_register_test.py
"""
    #TODO add comment
"""
import json
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.tac_register import FlowTacRegister, FlowTacRegisterResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
class TestTacRegisterPostModelResponse:
    """
    #TODO add comment
    """
    def test_flow_tac_register_result_to_json(self):
        """
            #TODO add comment
        """
        # Create an instance and set attributes
        result = FlowTacRegisterResult()
        result.context_object_code = uuid.uuid4()
        result.customer_code = uuid.uuid4()
        result.email = "test flavor"
        result.user_code_value = uuid.uuid4()
        result.utc_offset_in_minutes = 123
        result.role_name_csv_list = "test flavor"
        result.api_key = "test flavor"
# endset
        # Call to_json method
        json_output = result.to_json()
        # Parse JSON output
        data = json.loads(json_output)
        # Assert individual fields
        assert data["context_object_code"] == (
            str(result.context_object_code))
        assert data["customer_code"] == (
            str(result.customer_code))
        assert data["email"] == (
            result.email)
        assert data["user_code_value"] == (
            str(result.user_code_value))
        assert data["utc_offset_in_minutes"] == (
            result.utc_offset_in_minutes)
        assert data["role_name_csv_list"] == (
            result.role_name_csv_list)
        assert data["api_key"] == (
            result.api_key)
# endsets
    #TODO finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = FlowTacRegister(session_context)
        tac = await TacFactory.create_async(session)
        tac_bus_obj = TacBusObj(session_context)
        await tac_bus_obj.load_from_obj_instance(tac)
        role_required = ""
        email: str = ""
        password: str = ""
        confirm_password: str = ""
        first_name: str = ""
        last_name: str = ""
# endset
        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    tac_bus_obj,
                    email,
                    password,
                    confirm_password,
                    first_name,
                    last_name,
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
                    tac_bus_obj,
                    email,
                    password,
                    confirm_password,
                    first_name,
                    last_name,
# endset  # noqa: E122
                )
        session_context.role_name_csv = role_required
        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     tac_code=tac.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowTacRegisterResult)

