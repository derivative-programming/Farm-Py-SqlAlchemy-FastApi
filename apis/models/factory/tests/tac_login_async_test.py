# apis/models/factory/tests/tac_login_async_test.py

"""
This module contains test cases for the
TacLoginPostModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from ...tac_login import (
    TacLoginPostModelRequest)
from ..tac_login import (
    TacLoginPostModelRequestFactory)


class TestTacLoginPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    TacLoginPostModelRequestFactoryAsync class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        TacLoginPostModelRequestFactoryAsync class.
        """

        model_instance = (
            await TacLoginPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance,
                          TacLoginPostModelRequest)
        assert isinstance(model_instance.email,
                          str)
        assert isinstance(model_instance.password,
                          str)

