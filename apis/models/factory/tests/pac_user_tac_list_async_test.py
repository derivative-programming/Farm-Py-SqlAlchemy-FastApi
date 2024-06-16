# apis/models/factory/tests/pac_user_tac_list_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...pac_user_tac_list import PacUserTacListGetModelRequest
from ..pac_user_tac_list import PacUserTacListGetModelRequestFactory
class TestPacUserTacListGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
        """
        model_instance = await (
            PacUserTacListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance, PacUserTacListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
