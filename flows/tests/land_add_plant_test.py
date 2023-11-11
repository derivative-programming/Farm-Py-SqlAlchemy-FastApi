import asyncio
from decimal import Decimal
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
from services.db_config import db_dialect 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field,UUID4 
import flows.constants.error_log_config_resolve_error_log as FlowConstants
 
db_dialect = "sqlite"

# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
    
class TestLandAddPlantPostModelResponse:
 
    #todo finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session): 
        session_context = SessionContext(dict()) 
        flow = FlowLandAddPlant(session_context)
 
        land = await LandFactory.create_async(session)

        land_bus_obj = LandBusObj(session)
        await land_bus_obj.load(land_obj_instance=land)
        
        role_required = "User"


        request_flavor_code:uuid = uuid.UUID(int=0),    
        request_other_flavor:str = "",    
        request_some_int_val:int = 0,    
        request_some_big_int_val:int = 0,    
        request_some_bit_val:bool = False,    
        request_is_edit_allowed:bool = False,    
        request_is_delete_allowed:bool = False,    
        request_some_float_val:float = 0,    
        request_some_decimal_val:Decimal = 0,    
        request_some_utc_date_time_val:datetime = TypeConversion.get_default_date_time(),
        request_some_date_val:date = TypeConversion.get_default_date(),
        request_some_money_val:Decimal = 0,    
        request_some_n_var_char_val:str = "",    
        request_some_var_char_val:str = "",    
        request_some_text_val:str = "",    
        request_some_phone_number:str = "",    
        request_some_email_address:str = "",    
        request_sample_image_upload_file:str = "",
        
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
                ) 
        
        
        session_context.role_name_csv = role_required

        customerCodeMatchRequired = False 
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        
        if customerCodeMatchRequired == True: 
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
                ) 
 

        session_context.role_name_csv = role_required

        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     land_code=land.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowLandAddPlantResult)

