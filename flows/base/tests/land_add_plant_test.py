from decimal import Decimal
import uuid
import pytest
from decimal import Decimal
from datetime import datetime, date
from flows.base.land_add_plant import BaseFlowLandAddPlant
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.land import LandFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect
from sqlalchemy import String
import flows.constants.land_add_plant as FlowConstants
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestBaseFlowLandAddPlant():
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        session_context = SessionContext(dict(), session)
        flow = BaseFlowLandAddPlant(session_context)
        land = await LandFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)
        request_flavor_code:uuid = uuid.UUID(int=0)
        request_other_flavor:str = ""
        request_some_int_val:int = 0
        request_some_big_int_val:int = 0
        request_some_bit_val:bool = None
        request_is_edit_allowed:bool = None
        request_is_delete_allowed:bool = None
        request_some_float_val:float = 0
        request_some_decimal_val:Decimal = 0
        request_some_utc_date_time_val:datetime = TypeConversion.get_default_date_time()
        request_some_date_val:date = TypeConversion.get_default_date()
        request_some_money_val:Decimal = 0
        request_some_n_var_char_val:str = ""
        request_some_var_char_val:str = ""
        request_some_text_val:str = ""
        request_some_phone_number:str = ""
        request_some_email_address:str = ""
        request_sample_image_upload_file:str = ""
        # Call the method being tested
        await flow._process_validation_rules(
            land,
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
            )
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed
        if FlowConstants.param_request_flavor_code_isRequired == True:
            assert 'requestFlavorCode' in flow.queued_validation_errors and flow.queued_validation_errors['requestFlavorCode'] == 'Please select a Flavor'
        if FlowConstants.param_request_other_flavor_isRequired == True:
            assert 'requestOtherFlavor' in flow.queued_validation_errors and flow.queued_validation_errors['requestOtherFlavor'] == 'Please enter a Other Flavor'
        if FlowConstants.param_request_some_int_val_isRequired == True:
            assert 'requestSomeIntVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeIntVal'] == 'Please enter a Some Int Val'
        if FlowConstants.param_request_some_big_int_val_isRequired == True:
            assert 'requestSomeBigIntVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeBigIntVal'] == 'Please enter a Some Big Int Val'
        if FlowConstants.param_request_some_bit_val_isRequired == True:
            assert 'requestSomeBitVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeBitVal'] == 'Please enter a Some Bit Val'
        if FlowConstants.param_request_is_edit_allowed_isRequired == True:
            assert 'requestIsEditAllowed' in flow.queued_validation_errors and flow.queued_validation_errors['requestIsEditAllowed'] == 'Please enter a Is Edit Allowed'
        if FlowConstants.param_request_is_delete_allowed_isRequired == True:
            assert 'requestIsDeleteAllowed' in flow.queued_validation_errors and flow.queued_validation_errors['requestIsDeleteAllowed'] == 'Please enter a Is Delete Allowed'
        if FlowConstants.param_request_some_float_val_isRequired == True:
            assert 'requestSomeFloatVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeFloatVal'] == 'Please enter a Some Float Val'
        if FlowConstants.param_request_some_decimal_val_isRequired == True:
            assert 'requestSomeDecimalVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeDecimalVal'] == 'Please enter a Some Decimal Val'
        if FlowConstants.param_request_some_utc_date_time_val_isRequired == True:
            assert 'requestSomeUTCDateTimeVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeUTCDateTimeVal'] == 'Please enter a Some UTC Date Time Val'
        if FlowConstants.param_request_some_date_val_isRequired == True:
            assert 'requestSomeDateVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeDateVal'] == 'Please enter a Some Date Val'
        if FlowConstants.param_request_some_money_val_isRequired == True:
            assert 'requestSomeMoneyVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeMoneyVal'] == 'Please enter a Some Money Val'
        if FlowConstants.param_request_some_n_var_char_val_isRequired == True:
            assert 'requestSomeNVarCharVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeNVarCharVal'] == 'Please enter a Some N Var Char Val'
        if FlowConstants.param_request_some_var_char_val_isRequired == True:
            assert 'requestSomeVarCharVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeVarCharVal'] == 'Please enter a Some Var Char Val'
        if FlowConstants.param_request_some_text_val_isRequired == True:
            assert 'requestSomeTextVal' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeTextVal'] == 'Please enter a Some Text Val'
        if FlowConstants.param_request_some_phone_number_isRequired == True:
            assert 'requestSomePhoneNumber' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomePhoneNumber'] == 'Please enter a Some Phone Number'
        if FlowConstants.param_request_some_email_address_isRequired == True:
            assert 'requestSomeEmailAddress' in flow.queued_validation_errors and flow.queued_validation_errors['requestSomeEmailAddress'] == 'Please enter a Some Email Address'
        if FlowConstants.param_request_sample_image_upload_file_isRequired == True:
            assert 'requestSampleImageUploadFile' in flow.queued_validation_errors and flow.queued_validation_errors['requestSampleImageUploadFile'] == 'Please enter a image file'
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        session_context = SessionContext(dict(), session)
        land = await LandFactory.create_async(session)
        flow = BaseFlowLandAddPlant(session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(land)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
