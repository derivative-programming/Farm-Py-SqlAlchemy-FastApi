# reports/row_models/tests/tac_farm_dashboard_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemTacFarmDashboard` class.

The `ReportItemTacFarmDashboard` class represents a
report item for a tac Farm Dashboard.
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
from reports.row_models.tac_farm_dashboard import (
    ReportItemTacFarmDashboard)


class TestReportItemTacFarmDashboard:
    """
    Test class for the
    ReportItemTacFarmDashboard model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemTacFarmDashboard()
        assert report_item.field_one_plant_list_link_land_code.int == 0
        assert report_item.conditional_btn_example_link_land_code.int == 0
        assert report_item.is_conditional_btn_available is False
        assert report_item.test_file_download_link_pac_code.int == 0
        assert report_item.test_conditional_file_download_link_pac_code.int == 0
        assert report_item.test_async_flow_req_link_pac_code.int == 0
        assert report_item.test_conditional_async_flow_req_link_pac_code.int == 0

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "field_one_plant_list_link_land_code": str(UUID(int=5)),
            "conditional_btn_example_link_land_code": str(UUID(int=5)),
            "is_conditional_btn_available": True,
            "test_file_download_link_pac_code": str(UUID(int=4)),
            "test_conditional_file_download_link_pac_code": str(UUID(int=4)),
            "test_async_flow_req_link_pac_code": str(UUID(int=4)),
            "test_conditional_async_flow_req_link_pac_code": str(UUID(int=4)),
# endset  # noqa: E122
        }
        report_item = ReportItemTacFarmDashboard()
        report_item.load_data_provider_dict(data)
        assert report_item.field_one_plant_list_link_land_code == UUID(int=5)
        assert report_item.conditional_btn_example_link_land_code == UUID(int=5)
        assert report_item.is_conditional_btn_available is True
        assert report_item.test_file_download_link_pac_code == UUID(int=4)
        assert report_item.test_conditional_file_download_link_pac_code == UUID(int=4)
        assert report_item.test_async_flow_req_link_pac_code == UUID(int=4)
        assert report_item.test_conditional_async_flow_req_link_pac_code == UUID(int=4)
