# reports/row_models/tests/land_plant_list_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemLandPlantList` class.

The `ReportItemLandPlantList` class represents a
report item for a land plant list.
It contains various fields with default values and
provides methods to load data from a dictionary.

The unit tests in this module ensure that the default
values of the fields are set correctly
and that data can be loaded into the model from a dictionary.
"""
import math  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
from uuid import UUID  # noqa: F401
from helpers.type_conversion import TypeConversion  # noqa: F401
from reports.row_models.land_plant_list import (
    ReportItemLandPlantList)


class TestReportItemLandPlantList:
    """
    Test class for the
    ReportItemLandPlantList model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemLandPlantList()

        assert report_item.plant_code.int == 0
        assert report_item.some_int_val == 0
        assert report_item.some_big_int_val == 0
        assert report_item.some_bit_val is False
        assert report_item.is_edit_allowed is False
        assert report_item.is_delete_allowed is False
        assert math.isclose(report_item.some_float_val, 0.0, rel_tol=1e-9), (
            "Values must be approximately equal")
        assert report_item.some_decimal_val == Decimal(0)
        assert report_item.some_utc_date_time_val == (
            TypeConversion.get_default_date_time())
        assert report_item.some_date_val == TypeConversion.get_default_date()
        assert report_item.some_money_val == Decimal(0)
        assert report_item.some_n_var_char_val == ""
        assert report_item.some_var_char_val == ""
        assert report_item.some_text_val == ""
        assert report_item.some_phone_number == ""
        assert report_item.some_email_address == ""
        assert report_item.flavor_name == ""
        assert report_item.flavor_code.int == 0
        assert report_item.some_int_conditional_on_deletable == 0
        assert report_item.n_var_char_as_url == ""
        assert report_item.update_link_plant_code.int == 0
        assert report_item.delete_async_button_link_plant_code.int == 0
        assert report_item.details_link_plant_code.int == 0
        assert report_item.test_file_download_link_pac_code.int == 0
        assert report_item.test_conditional_file_download_link_pac_code.int == 0
        assert report_item.test_async_flow_req_link_pac_code.int == 0
        assert report_item.test_conditional_async_flow_req_link_pac_code.int == 0
        assert report_item.conditional_btn_example_link_plant_code.int == 0
# endset

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "plant_code": str(UUID(int=1)),
            "some_int_val": 1,
            "some_big_int_val": 1000000000,
            "some_bit_val": True,
            "is_edit_allowed": True,
            "is_delete_allowed": True,
            "some_float_val": 1.23,
            "some_decimal_val": "10.99",
            "some_utc_date_time_val":
                datetime(2023, 1, 1, 0, 0, 0),  # "2023-01-01T00:00:00",
            "some_date_val": date(2023, 1, 1),  # "2023-01-01",
            "some_money_val": "99.99",
            "some_n_var_char_val": "test",
            "some_var_char_val": "test",
            "some_text_val": "test",
            "some_phone_number": "1234567890",
            "some_email_address": "test@example.com",
            "flavor_name": "Vanilla",
            "flavor_code": str(UUID(int=2)),
            "some_int_conditional_on_deletable": 10,
            "n_var_char_as_url": "https://example.com",
            "update_link_plant_code": str(UUID(int=3)),
            "delete_async_button_link_plant_code": str(UUID(int=4)),
            "details_link_plant_code": str(UUID(int=5)),
            "test_file_download_link_pac_code": str(UUID(int=5)),
            "test_conditional_file_download_link_pac_code": str(UUID(int=5)),
            "test_async_flow_req_link_pac_code": str(UUID(int=5)),
            "test_conditional_async_flow_req_link_pac_code": str(UUID(int=5)),
            "conditional_btn_example_link_plant_code": str(UUID(int=5)),
# endset  # noqa: E122
        }
        report_item = ReportItemLandPlantList()
        report_item.load_data_provider_dict(data)

        assert report_item.plant_code == UUID(int=1)
        assert report_item.some_int_val == 1
        assert report_item.some_big_int_val == 1000000000
        assert report_item.some_bit_val is True
        assert report_item.is_edit_allowed is True
        assert report_item.is_delete_allowed is True
        assert math.isclose(report_item.some_float_val, 1.23, rel_tol=1e-9), (
            "Values must be approximately equal")
        assert report_item.some_decimal_val == Decimal("10.99")
        assert report_item.some_utc_date_time_val == (
            datetime.fromisoformat("2023-01-01T00:00:00"))
        assert report_item.some_date_val == date.fromisoformat("2023-01-01")
        assert report_item.some_money_val == Decimal("99.99")
        assert report_item.some_n_var_char_val == "test"
        assert report_item.some_var_char_val == "test"
        assert report_item.some_text_val == "test"
        assert report_item.some_phone_number == "1234567890"
        assert report_item.some_email_address == "test@example.com"
        assert report_item.flavor_name == "Vanilla"
        assert report_item.flavor_code == UUID(int=2)
        assert report_item.some_int_conditional_on_deletable == 10
        assert report_item.n_var_char_as_url == "https://example.com"
        assert report_item.update_link_plant_code == UUID(int=3)
        assert report_item.delete_async_button_link_plant_code == UUID(int=4)
        assert report_item.details_link_plant_code == UUID(int=5)
        assert report_item.test_file_download_link_pac_code == UUID(int=5)
        assert report_item.test_conditional_file_download_link_pac_code == UUID(int=5)
        assert report_item.test_async_flow_req_link_pac_code == UUID(int=5)
        assert report_item.test_conditional_async_flow_req_link_pac_code == UUID(int=5)
        assert report_item.conditional_btn_example_link_plant_code == UUID(int=5)
# endset
