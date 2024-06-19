# apis/models/tests/pac_user_date_greater_than_filter_list_test.py
"""
This module contains unit tests for the
PacUserDateGreaterThanFilterListGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListGetModelRequestFactory
from ..pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListGetModelRequest
class PacUserDateGreaterThanFilterListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserDateGreaterThanFilterListGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserDateGreaterThanFilterListGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            PacUserDateGreaterThanFilterListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PacUserDateGreaterThanFilterListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
