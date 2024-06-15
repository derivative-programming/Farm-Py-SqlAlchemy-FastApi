# apis/models/factory/tests/tac_login_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...tac_login import TacLoginPostModelRequest
from ..tac_login import TacLoginPostModelRequestFactory
class TestTacLoginPostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
        """
        model_instance = (
            await TacLoginPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, TacLoginPostModelRequest)
        assert isinstance(model_instance.email,
                          str)
        assert isinstance(model_instance.password,
                          str)

