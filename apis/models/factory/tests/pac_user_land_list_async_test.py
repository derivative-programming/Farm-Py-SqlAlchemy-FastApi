# apis/models/factory/tests/pac_user_land_list_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
PacUserLandListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_user_land_list import (
    PacUserLandListGetModelRequest)
from ..pac_user_land_list import (
    PacUserLandListGetModelRequestFactory)


class TestPacUserLandListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserLandListGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserLandListGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            PacUserLandListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          PacUserLandListGetModelRequest)

