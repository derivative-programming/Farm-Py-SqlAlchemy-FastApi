import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio 
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from ...land_plant_list import LandPlantListGetModelRequest
from models import Base
from ..land_plant_list import LandPlantListGetModelRequestFactory
from services.db_config import db_dialect 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field,UUID4 

db_dialect = "sqlite"

# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
    
class TestLandPlantListGetModelRequestFactoryAsync: 
  
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        model_instance = await LandPlantListGetModelRequestFactory.create_async(session=session)
        assert isinstance(model_instance,LandPlantListGetModelRequest)
        assert isinstance(model_instance.flavor_code,str) 
        assert isinstance(model_instance.some_int_val,int)
        assert isinstance(model_instance.some_big_int_val,int)
        assert isinstance(model_instance.some_float_val,float)
        assert isinstance(model_instance.some_bit_val,bool)
        assert isinstance(model_instance.is_edit_allowed,bool)
        assert isinstance(model_instance.is_delete_allowed,bool)
        assert isinstance(model_instance.some_decimal_val,Decimal)
        assert isinstance(model_instance.some_min_utc_date_time_val,datetime)
        assert isinstance(model_instance.some_min_date_val,date)
        assert isinstance(model_instance.some_money_val,Decimal)
        assert isinstance(model_instance.some_n_var_char_val,str)
        assert isinstance(model_instance.some_var_char_val,str)
        assert isinstance(model_instance.some_text_val,str)
        assert isinstance(model_instance.some_phone_number,str)
        assert isinstance(model_instance.some_email_address,str)
        assert isinstance(model_instance.page_number,int)
        assert isinstance(model_instance.item_count_per_page,int)
 