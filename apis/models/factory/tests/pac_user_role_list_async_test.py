# apis/models/factory/tests/pac_user_role_list_async_test.py
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
from ...pac_user_role_list import PacUserRoleListGetModelRequest
from ..pac_user_role_list import PacUserRoleListGetModelRequestFactory
class TestPacUserRoleListGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        model_instance = await PacUserRoleListGetModelRequestFactory.create_async(session=session)
        assert isinstance(model_instance, PacUserRoleListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
