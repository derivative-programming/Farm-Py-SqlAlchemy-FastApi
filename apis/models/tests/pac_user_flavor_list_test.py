# apis/models/tests/pac_user_flavor_list_test.py
"""
This module contains unit tests for the
PacUserFlavorListGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.pac_user_flavor_list import PacUserFlavorListGetModelRequestFactory
from ..pac_user_flavor_list import PacUserFlavorListGetModelRequest
class PacUserFlavorListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserFlavorListGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserFlavorListGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            PacUserFlavorListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PacUserFlavorListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
