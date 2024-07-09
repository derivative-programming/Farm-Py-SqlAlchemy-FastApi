# business/land_reports.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the LandReportsBusObj class
which provides methods to generate various reports
related to Land objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Land

from .land_fluent import LandFluentBusObj


class LandReportsBusObj(LandFluentBusObj):
    """
    This class extends the LandFluentBusObj class
    and provides methods to generate various reports
    related to Land objects.
    """


    async def generate_report_land_plant_list(
        self,
        flavor_code:
            uuid.UUID = uuid.UUID(int=0),
        some_int_val:
            int = 0,
        some_big_int_val:
            int = 0,
        some_float_val:
            float = 0,
        some_bit_val:
            bool = False,
        is_edit_allowed:
            bool = False,
        is_delete_allowed:
            bool = False,
        some_decimal_val:
            Decimal = Decimal(0),
        some_min_utc_date_time_val:
            datetime = TypeConversion.get_default_date_time(),
        some_min_date_val:
            date = TypeConversion.get_default_date(),
        some_money_val:
            Decimal = Decimal(0),
        some_n_var_char_val:
            str = "",
        some_var_char_val:
            str = "",
        some_text_val:
            str = "",
        some_phone_number:
            str = "",
        some_email_address:
            str = "",
        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemLandPlantList]:
        """
        Get the Land Plant List report.

        Returns:
            List[ReportItemLandPlantList]:
                The Land Plant List report.
        """
        report_manager = reports_managers. \
            ReportManagerLandPlantList(
                self._session_context)
        return await report_manager.generate(
            self.code,
            flavor_code,
            some_int_val,
            some_big_int_val,
            some_float_val,
            some_bit_val,
            is_edit_allowed,
            is_delete_allowed,
            some_decimal_val,
            some_min_utc_date_time_val,
            some_min_date_val,
            some_money_val,
            some_n_var_char_val,
            some_var_char_val,
            some_text_val,
            some_phone_number,
            some_email_address,
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
