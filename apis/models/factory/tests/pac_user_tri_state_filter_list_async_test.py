# apis/models/factory/tests/pac_user_tri_state_filter_list_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
PacUserTriStateFilterListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_user_tri_state_filter_list import (
    PacUserTriStateFilterListGetModelRequest)
from ..pac_user_tri_state_filter_list import (
    PacUserTriStateFilterListGetModelRequestFactory)


class TestPacUserTriStateFilterListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserTriStateFilterListGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserTriStateFilterListGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            PacUserTriStateFilterListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          PacUserTriStateFilterListGetModelRequest)

