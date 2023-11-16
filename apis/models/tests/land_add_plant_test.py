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
from ...models.land_add_plant import LandAddPlantPostModelRequest,LandAddPlantPostModelResponse
from models import Base
from ..factory.land_add_plant import LandAddPlantPostModelRequestFactory
from services.db_config import db_dialect 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field,UUID4 
import flows.constants.error_log_config_resolve_error_log as FlowConstants 
from unittest.mock import patch, AsyncMock

db_dialect = "sqlite"

# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
    
class TestLandAddPlantPostModelResponse:
 
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        async def mock_process( 
            land_bus_obj: LandBusObj,
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
            ):
            return FlowLandAddPlantResult()
        with patch.object(FlowLandAddPlant, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process
            
            request_instance = await LandAddPlantPostModelRequestFactory.create_async(session=session) 
            response_instance = LandAddPlantPostModelResponse()
            session_context = SessionContext(dict(), session) 
            
            land = await LandFactory.create_async(session) 

            await response_instance.process_request( 
                session_context=session_context,
                land_code=land.code,
                request=request_instance
                )
            assert response_instance.success == True
            mock_method.assert_awaited()

