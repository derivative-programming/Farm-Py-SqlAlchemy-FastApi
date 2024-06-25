# apis/models/factory/tests/pac_user_land_list_async_test.py

"""
This module contains test cases for the
PacUserLandListGetModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from ...pac_user_land_list import (
    PacUserLandListGetModelRequest)
from ..pac_user_land_list import (
    PacUserLandListGetModelRequestFactory)


class TestPacUserLandListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserLandListGetModelRequestFactoryAsync class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserLandListGetModelRequestFactoryAsync class.
        """

        model_instance = await (
            PacUserLandListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          PacUserLandListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)

