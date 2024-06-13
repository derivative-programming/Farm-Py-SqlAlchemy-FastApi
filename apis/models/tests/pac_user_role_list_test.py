# apis/models/tests/pac_user_role_list_test.py
"""
    #TODO add comment
"""
import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from ..pac_user_role_list import PacUserRoleListGetModelRequest
from models import Base
from ..factory.pac_user_role_list import PacUserRoleListGetModelRequestFactory
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
class PacUserRoleListGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        model_instance = await PacUserRoleListGetModelRequestFactory.create_async(session=session)
        assert isinstance(model_instance, PacUserRoleListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
