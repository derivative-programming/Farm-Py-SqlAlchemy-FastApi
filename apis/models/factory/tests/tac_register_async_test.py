# apis/models/factory/tests/tac_register_async_test.py
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
from ...tac_register import TacRegisterPostModelRequest
from models import Base
from ..tac_register import TacRegisterPostModelRequestFactory
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
DB_DIALECT = "sqlite"  # noqa: F811
class TestTacRegisterPostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        model_instance = (
            await TacRegisterPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, TacRegisterPostModelRequest)
        assert isinstance(model_instance.email,
                          str)
        assert isinstance(model_instance.password,
                          str)
        assert isinstance(model_instance.confirm_password,
                          str)
        assert isinstance(model_instance.first_name,
                          str)
        assert isinstance(model_instance.last_name,
                          str)

