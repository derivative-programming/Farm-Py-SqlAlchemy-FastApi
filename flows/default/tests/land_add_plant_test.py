# flows/default/tests/land_add_plant_test.py

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
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_add_plant import FlowLandAddPlant, FlowLandAddPlantResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.land import LandFactory
from models import Base
from services.db_config import DB_DIALECT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants

DB_DIALECT = "sqlite"

# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)


class TestLandAddPlantPostModelResponse:
    """
    #TODO add comment
    """

    def test_flow_land_add_plant_result_to_json(self):
        # Create an instance and set attributes
        result = FlowLandAddPlantResult()
        result.context_object_code = uuid.uuid4()
        result.land_code = uuid.uuid4()
        result.plant_code = uuid.uuid4()
        result.output_flavor_code = uuid.uuid4()
        result.output_other_flavor = "test flavor"
        result.output_some_int_val = 123
        result.output_some_big_int_val = 123456789
        result.output_some_bit_val = True
        result.output_is_edit_allowed = True
        result.output_is_delete_allowed = False
        result.output_some_float_val = 12.34
        result.output_some_decimal_val = Decimal("123.45")
        result.output_some_utc_date_time_val = datetime.utcnow()
        result.output_some_date_val = date.today()
        result.output_some_money_val = Decimal("67.89")
        result.output_some_n_var_char_val = "nvarchar test"
        result.output_some_var_char_val = "varchar test"
        result.output_some_text_val = "text value"
        result.output_some_phone_number = "123-456-7890"
        result.output_some_email_address = "test@example.com"
# endset

        # Call to_json method
        json_output = result.to_json()

        # Parse JSON output
        data = json.loads(json_output)

        # Assert individual fields
        assert data["context_object_code"] == str(result.context_object_code)
        assert data["land_code"] == str(result.land_code)
        assert data["plant_code"] == str(result.plant_code)
        assert data["output_flavor_code"] == str(result.output_flavor_code)
        assert data["output_other_flavor"] == result.output_other_flavor
        assert data["output_some_int_val"] == result.output_some_int_val
        assert data["output_some_big_int_val"] == result.output_some_big_int_val
        assert data["output_some_bit_val"] == result.output_some_bit_val
        assert data["output_is_edit_allowed"] == result.output_is_edit_allowed
        assert data["output_is_delete_allowed"] == result.output_is_delete_allowed
        assert data["output_some_float_val"] == result.output_some_float_val
        assert data["output_some_decimal_val"] == str(result.output_some_decimal_val)
        assert data["output_some_utc_date_time_val"] == result.output_some_utc_date_time_val.isoformat()
        assert data["output_some_date_val"] == result.output_some_date_val.isoformat()
        assert data["output_some_money_val"] == str(result.output_some_money_val)
        assert data["output_some_n_var_char_val"] == result.output_some_n_var_char_val
        assert data["output_some_var_char_val"] == result.output_some_var_char_val
        assert data["output_some_text_val"] == result.output_some_text_val
        assert data["output_some_phone_number"] == result.output_some_phone_number
        assert data["output_some_email_address"] == result.output_some_email_address
# endset

    #todo finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        session_context = SessionContext(dict(), session)
        flow = FlowLandAddPlant(session_context)

        land = await LandFactory.create_async(session)

        land_bus_obj = LandBusObj(session_context)
        await land_bus_obj.load(land_obj_instance=land)

        role_required = "User"


        request_flavor_code: uuid = uuid.UUID(int=0),
        request_other_flavor: str = "",
        request_some_int_val: int = 0,
        request_some_big_int_val: int = 0,
        request_some_bit_val: bool = False,
        request_is_edit_allowed: bool = False,
        request_is_delete_allowed: bool = False,
        request_some_float_val: float = 0,
        request_some_decimal_val: Decimal = 0,
        request_some_utc_date_time_val: datetime = TypeConversion.get_default_date_time(),
        request_some_date_val: date = TypeConversion.get_default_date(),
        request_some_money_val: Decimal = 0,
        request_some_n_var_char_val: str = "",
        request_some_var_char_val: str = "",
        request_some_text_val: str = "",
        request_some_phone_number: str = "",
        request_some_email_address: str = "",
        request_sample_image_upload_file: str = "",
# endset

        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    land_bus_obj,
                    request_flavor_code,
                    request_other_flavor,
                    request_some_int_val,
                    request_some_big_int_val,
                    request_some_bit_val,
                    request_is_edit_allowed,
                    request_is_delete_allowed,
                    request_some_float_val,
                    request_some_decimal_val,
                    request_some_utc_date_time_val,
                    request_some_date_val,
                    request_some_money_val,
                    request_some_n_var_char_val,
                    request_some_var_char_val,
                    request_some_text_val,
                    request_some_phone_number,
                    request_some_email_address,
                    request_sample_image_upload_file,
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
                    request_flavor_code,
                    request_other_flavor,
                    request_some_int_val,
                    request_some_big_int_val,
                    request_some_bit_val,
                    request_is_edit_allowed,
                    request_is_delete_allowed,
                    request_some_float_val,
                    request_some_decimal_val,
                    request_some_utc_date_time_val,
                    request_some_date_val,
                    request_some_money_val,
                    request_some_n_var_char_val,
                    request_some_var_char_val,
                    request_some_text_val,
                    request_some_phone_number,
                    request_some_email_address,
                    request_sample_image_upload_file,
# endset
                )


        session_context.role_name_csv = role_required

        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     land_code=land.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowLandAddPlantResult)
