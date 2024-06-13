# apis/models/factory/tests/plant_user_details_async_test.py
"""
    #TODO add comment
"""
import asyncio
import time
from datetime import date, datetime
from decimal import Decimal
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from pydantic import UUID4, Field
from sqlalchemy import String, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from models import Base
from ...plant_user_details import PlantUserDetailsGetModelRequest
from ..plant_user_details import PlantUserDetailsGetModelRequestFactory
class TestPlantUserDetailsGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        model_instance = await PlantUserDetailsGetModelRequestFactory.create_async(session=session)
        assert isinstance(model_instance, PlantUserDetailsGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
