# apis/models/factory/tests/pac_user_flavor_list_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
PacUserFlavorListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_user_flavor_list import (
    PacUserFlavorListGetModelRequest)
from ..pac_user_flavor_list import (
    PacUserFlavorListGetModelRequestFactory)


class TestPacUserFlavorListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserFlavorListGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserFlavorListGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            PacUserFlavorListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(
            model_instance,
            PacUserFlavorListGetModelRequest)
