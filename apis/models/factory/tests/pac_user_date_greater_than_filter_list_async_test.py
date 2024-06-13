# apis/models/factory/tests/pac_user_date_greater_than_filter_list_async_test.py
"""
    #TODO add comment
"""
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
from ...pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListGetModelRequest
from models import Base
from ..pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListGetModelRequestFactory
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
class TestPacUserDateGreaterThanFilterListGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        model_instance = await PacUserDateGreaterThanFilterListGetModelRequestFactory.create_async(session=session)
        assert isinstance(model_instance, PacUserDateGreaterThanFilterListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
