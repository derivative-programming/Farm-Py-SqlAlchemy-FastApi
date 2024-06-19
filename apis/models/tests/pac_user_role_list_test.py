# apis/models/tests/pac_user_role_list_test.py
"""
This module contains unit tests for the
PacUserRoleListGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.pac_user_role_list import PacUserRoleListGetModelRequestFactory
from ..pac_user_role_list import PacUserRoleListGetModelRequest
class PacUserRoleListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserRoleListGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserRoleListGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            PacUserRoleListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PacUserRoleListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
