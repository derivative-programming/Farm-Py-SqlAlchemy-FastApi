# apis/models/factory/tests/tac_login_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
TacLoginPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...tac_login import (
    TacLoginPostModelRequest)
from ..tac_login import (
    TacLoginPostModelRequestFactory)


class TestTacLoginPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    TacLoginPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        TacLoginPostModelRequestFactoryAsync
        class.
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

