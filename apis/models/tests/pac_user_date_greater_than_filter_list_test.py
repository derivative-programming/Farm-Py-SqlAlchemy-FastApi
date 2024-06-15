# apis/models/tests/pac_user_date_greater_than_filter_list_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListGetModelRequestFactory
from ..pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListGetModelRequest
class PacUserDateGreaterThanFilterListGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
            #TODO add comment
        """
        model_instance = await PacUserDateGreaterThanFilterListGetModelRequestFactory.create_async(session=session)
        assert isinstance(model_instance, PacUserDateGreaterThanFilterListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
