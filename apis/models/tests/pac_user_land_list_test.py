# apis/models/tests/pac_user_land_list_test.py
"""
This module contains unit tests for the
PacUserLandListGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.pac_user_land_list import PacUserLandListGetModelRequestFactory
from ..pac_user_land_list import PacUserLandListGetModelRequest
class PacUserLandListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserLandListGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserLandListGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            PacUserLandListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PacUserLandListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
