# apis/models/factory/tests/pac_user_tac_list_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
PacUserTacListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_user_tac_list import (
    PacUserTacListGetModelRequest)
from ..pac_user_tac_list import (
    PacUserTacListGetModelRequestFactory)


class TestPacUserTacListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserTacListGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserTacListGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            PacUserTacListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          PacUserTacListGetModelRequest)

