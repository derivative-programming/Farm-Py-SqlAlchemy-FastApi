# apis/models/factory/tests/land_add_plant_async_test.py

"""
    #TODO add comment
"""

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
from ...land_add_plant import LandAddPlantPostModelRequest
from models import Base
from ..land_add_plant import LandAddPlantPostModelRequestFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4

db_dialect = "sqlite"

# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)

class TestLandAddPlantPostModelRequestFactoryAsync:

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        model_instance = await LandAddPlantPostModelRequestFactory.create_async(session=session)
        assert isinstance(model_instance, LandAddPlantPostModelRequest)
        assert isinstance(model_instance.request_flavor_code, str)
        assert isinstance(model_instance.request_other_flavor, str)
        assert isinstance(model_instance.request_some_int_val, int)
        assert isinstance(model_instance.request_some_big_int_val, int)
        assert isinstance(model_instance.request_some_bit_val, bool)
        assert isinstance(model_instance.request_is_edit_allowed, bool)
        assert isinstance(model_instance.request_is_delete_allowed, bool)
        assert isinstance(model_instance.request_some_float_val, float)
        assert isinstance(model_instance.request_some_decimal_val, Decimal)
        assert isinstance(model_instance.request_some_utc_date_time_val, datetime)
        assert isinstance(model_instance.request_some_date_val, date)
        assert isinstance(model_instance.request_some_money_val, Decimal)
        assert isinstance(model_instance.request_some_n_var_char_val, str)
        assert isinstance(model_instance.request_some_var_char_val, str)
        assert isinstance(model_instance.request_some_text_val, str)
        assert isinstance(model_instance.request_some_phone_number, str)
        assert isinstance(model_instance.request_some_email_address, str)
        assert isinstance(model_instance.request_sample_image_upload_file, str)
