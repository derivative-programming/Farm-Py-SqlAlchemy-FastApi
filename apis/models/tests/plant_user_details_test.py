# apis/models/tests/plant_user_details_test.py
"""
This module contains unit tests for the
PlantUserDetailsGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from helpers.type_conversion import TypeConversion
from ..factory.plant_user_details import PlantUserDetailsGetModelRequestFactory
from ..plant_user_details import PlantUserDetailsGetModelRequest
class TestPlantUserDetailsGetModelRequest():
    def test_default_values(self):
        model = PlantUserDetailsGetModelRequest()
        assert model.page_number == 0
        assert model.item_count_per_page == 0
        assert model.order_by_column_name == ""
        assert model.order_by_descending is False
        assert model.force_error_message == ""
# endset

# endset
    def test_to_dict_snake(self):
        model = PlantUserDetailsGetModelRequest(
            page_number=1,
            item_count_per_page=10,
            order_by_column_name="name",
            order_by_descending=True,
            force_error_message="Test Error",
# endset

# endset
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['page_number'] == 1
        assert snake_case_dict['item_count_per_page'] == 10
        assert snake_case_dict['order_by_column_name'] == "name"
        assert snake_case_dict['order_by_descending'] is True
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset

# endset
    def test_to_dict_camel(self):
        model = PlantUserDetailsGetModelRequest(
            page_number=1,
            item_count_per_page=10,
            order_by_column_name="name",
            order_by_descending=True,
            force_error_message="Test Error",
# endset

# endset
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['pageNumber'] == 1
        assert camel_case_dict['itemCountPerPage'] == 10
        assert camel_case_dict['orderByColumnName'] == "name"
        assert camel_case_dict['orderByDescending'] is True
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset

# endset
class PlantUserDetailsGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PlantUserDetailsGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PlantUserDetailsGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            PlantUserDetailsGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PlantUserDetailsGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
