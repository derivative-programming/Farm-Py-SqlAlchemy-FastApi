# apis/models/factory/tests/pac_user_tac_list_async_test.py

"""
This module contains test cases for the
PacUserTacListGetModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from ...pac_user_tac_list import (
    PacUserTacListGetModelRequest)
from ..pac_user_tac_list import (
    PacUserTacListGetModelRequestFactory)


class TestPacUserTacListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserTacListGetModelRequestFactoryAsync class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserTacListGetModelRequestFactoryAsync class.
        """

        model_instance = await (
            PacUserTacListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          PacUserTacListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)

