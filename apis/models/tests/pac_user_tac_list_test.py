# apis/models/tests/pac_user_tac_list_test.py
"""
This module contains unit tests for the
PacUserTacListGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.pac_user_tac_list import PacUserTacListGetModelRequestFactory
from ..pac_user_tac_list import PacUserTacListGetModelRequest
class PacUserTacListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserTacListGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserTacListGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            PacUserTacListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PacUserTacListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
