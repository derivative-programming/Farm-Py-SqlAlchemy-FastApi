# apis/models/factory/tests/land_user_plant_multi_select_to_editable_async_test.py
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
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from ...land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditablePostModelRequest
from models import Base
from ..land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditablePostModelRequestFactory
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
class TestLandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        model_instance = (
            await LandUserPlantMultiSelectToEditablePostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, LandUserPlantMultiSelectToEditablePostModelRequest)
        assert isinstance(model_instance.plant_code_list_csv,
                          str)

