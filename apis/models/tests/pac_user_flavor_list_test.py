# apis/models/tests/pac_user_flavor_list_test.py
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
from ..pac_user_flavor_list import PacUserFlavorListGetModelRequest
from models import Base
from ..factory.pac_user_flavor_list import PacUserFlavorListGetModelRequestFactory
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
DB_DIALECT = "sqlite"  # noqa: F811
class PacUserFlavorListGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        model_instance = await PacUserFlavorListGetModelRequestFactory.create_async(session=session)
        assert isinstance(model_instance, PacUserFlavorListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
