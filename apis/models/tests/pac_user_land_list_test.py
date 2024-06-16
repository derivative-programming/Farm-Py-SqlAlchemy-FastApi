# apis/models/tests/pac_user_land_list_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.pac_user_land_list import PacUserLandListGetModelRequestFactory
from ..pac_user_land_list import PacUserLandListGetModelRequest
class PacUserLandListGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
            #TODO add comment
        """
        model_instance = await (
            PacUserLandListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PacUserLandListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
