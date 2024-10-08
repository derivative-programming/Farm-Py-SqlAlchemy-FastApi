# reports/row_models/tests/plant_user_details_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemPlantUserDetails` class.

The `ReportItemPlantUserDetails` class represents a
report item for a plant Plant Details.
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
from reports.row_models.plant_user_details import (
    ReportItemPlantUserDetails)


class TestReportItemPlantUserDetails:
    """
    Test class for the
    ReportItemPlantUserDetails model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPlantUserDetails()
        assert report_item.flavor_name == ""
        assert report_item.is_delete_allowed is False
        assert report_item.is_edit_allowed is False
        assert report_item.other_flavor == ""
        assert report_item.some_big_int_val == 0
        assert report_item.some_bit_val is False
        assert report_item.some_date_val == TypeConversion.get_default_date()
        assert report_item.some_decimal_val == Decimal(0)
        assert report_item.some_email_address == ""
        assert math.isclose(report_item.some_float_val, 0.0, rel_tol=1e-9), (
            "Values must be approximately equal")
        assert report_item.some_int_val == 0
        assert report_item.some_money_val == Decimal(0)
        assert report_item.some_n_var_char_val == ""
        assert report_item.some_phone_number == ""
        assert report_item.some_text_val == ""
        assert report_item.some_uniqueidentifier_val.int == 0
        assert report_item.some_utc_date_time_val == (
            TypeConversion.get_default_date_time())
        assert report_item.some_var_char_val == ""
        assert report_item.phone_num_conditional_on_is_editable == ""
        assert report_item.n_var_char_as_url == ""
        assert report_item.update_button_text_link_plant_code.int == 0
        assert report_item.random_property_updates_link_plant_code.int == 0
        assert report_item.back_to_dashboard_link_tac_code.int == 0
        assert report_item.test_file_download_link_pac_code.int == 0
        assert report_item.test_conditional_async_file_download_link_pac_code.int == 0
        assert report_item.test_async_flow_req_link_pac_code.int == 0
        assert report_item.test_conditional_async_flow_req_link_pac_code.int == 0
        assert report_item.conditional_btn_example_link_tac_code.int == 0

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "flavor_name": "test",
            "is_delete_allowed": True,
            "is_edit_allowed": True,
            "other_flavor": "test",
            "some_big_int_val": 1000000000,
            "some_bit_val": True,
            "some_date_val": date(2023, 1, 1),  # "2023-01-01",
            "some_decimal_val": "10.99",
            "some_email_address": "test@example.com",
            "some_float_val": 1.23,
            "some_int_val": 1,
            "some_money_val": "99.99",
            "some_n_var_char_val": "test",
            "some_phone_number": "1234567890",
            "some_text_val": "test",
            "some_uniqueidentifier_val": str(UUID(int=2)),
            "some_utc_date_time_val":
                datetime(2023, 1, 1, 0, 0, 0),  # "2023-01-01T00:00:00",
            "some_var_char_val": "test",
            "phone_num_conditional_on_is_editable": "test",
            "n_var_char_as_url": "https://example.com",
            "update_button_text_link_plant_code": str(UUID(int=5)),
            "random_property_updates_link_plant_code": str(UUID(int=4)),
            "back_to_dashboard_link_tac_code": str(UUID(int=5)),
            "test_file_download_link_pac_code": str(UUID(int=4)),
            "test_conditional_async_file_download_link_pac_code": str(UUID(int=4)),
            "test_async_flow_req_link_pac_code": str(UUID(int=4)),
            "test_conditional_async_flow_req_link_pac_code": str(UUID(int=4)),
            "conditional_btn_example_link_tac_code": str(UUID(int=5)),
# endset  # noqa: E122
        }
        report_item = ReportItemPlantUserDetails()
        report_item.load_data_provider_dict(data)
        assert report_item.flavor_name == "test"
        assert report_item.is_delete_allowed is True
        assert report_item.is_edit_allowed is True
        assert report_item.other_flavor == "test"
        assert report_item.some_big_int_val == 1000000000
        assert report_item.some_bit_val is True
        assert report_item.some_date_val == date.fromisoformat("2023-01-01")
        assert report_item.some_decimal_val == Decimal("10.99")
        assert report_item.some_email_address == "test@example.com"
        assert math.isclose(report_item.some_float_val, 1.23, rel_tol=1e-9), (
            "Values must be approximately equal")
        assert report_item.some_int_val == 1
        assert report_item.some_money_val == Decimal("99.99")
        assert report_item.some_n_var_char_val == "test"
        assert report_item.some_phone_number == "1234567890"
        assert report_item.some_text_val == "test"
        assert report_item.some_uniqueidentifier_val == UUID(int=2)
        assert report_item.some_utc_date_time_val == (
            datetime.fromisoformat("2023-01-01T00:00:00"))
        assert report_item.some_var_char_val == "test"
        assert report_item.phone_num_conditional_on_is_editable == "test"
        assert report_item.n_var_char_as_url == "https://example.com"
        assert report_item.update_button_text_link_plant_code == UUID(int=5)
        assert report_item.random_property_updates_link_plant_code == UUID(int=4)
        assert report_item.back_to_dashboard_link_tac_code == UUID(int=5)
        assert report_item.test_file_download_link_pac_code == UUID(int=4)
        assert report_item.test_conditional_async_file_download_link_pac_code == UUID(int=4)
        assert report_item.test_async_flow_req_link_pac_code == UUID(int=4)
        assert report_item.test_conditional_async_flow_req_link_pac_code == UUID(int=4)
        assert report_item.conditional_btn_example_link_tac_code == UUID(int=5)
