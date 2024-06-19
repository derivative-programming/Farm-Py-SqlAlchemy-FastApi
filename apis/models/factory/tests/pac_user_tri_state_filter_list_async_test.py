# apis/models/factory/tests/pac_user_tri_state_filter_list_async_test.py
"""
This module contains test cases for the
PacUserTriStateFilterListGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...pac_user_tri_state_filter_list import PacUserTriStateFilterListGetModelRequest
from ..pac_user_tri_state_filter_list import PacUserTriStateFilterListGetModelRequestFactory
class TestPacUserTriStateFilterListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserTriStateFilterListGetModelRequestFactoryAsync class.
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserTriStateFilterListGetModelRequestFactoryAsync class.
        """
        model_instance = await (
            PacUserTriStateFilterListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance, PacUserTriStateFilterListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
