# apis/models/factory/tests/customer_build_temp_api_key_async_test.py
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
from ...customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequest
from models import Base
from ..customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequestFactory
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
class TestCustomerBuildTempApiKeyPostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        model_instance = (
            await CustomerBuildTempApiKeyPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, CustomerBuildTempApiKeyPostModelRequest)

