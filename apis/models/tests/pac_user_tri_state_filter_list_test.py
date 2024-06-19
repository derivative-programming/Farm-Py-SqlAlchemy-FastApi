# apis/models/tests/pac_user_tri_state_filter_list_test.py
"""
This module contains unit tests for the
PacUserTriStateFilterListGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.pac_user_tri_state_filter_list import PacUserTriStateFilterListGetModelRequestFactory
from ..pac_user_tri_state_filter_list import PacUserTriStateFilterListGetModelRequest
class PacUserTriStateFilterListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserTriStateFilterListGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserTriStateFilterListGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            PacUserTriStateFilterListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PacUserTriStateFilterListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
