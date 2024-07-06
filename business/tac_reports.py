# business/tac_reports.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the TacReportsBusObj class
which provides methods to generate various reports
related to Tac objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Tac

from .tac_fluent import TacFluentBusObj


class TacReportsBusObj(TacFluentBusObj):
    """
    This class extends the TacFluentBusObj class
    and provides methods to generate various reports
    related to Tac objects.
    """


    async def generate_report_tac_farm_dashboard(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemTacFarmDashboard]:
        """
        Get the Tac Farm Dashboard report.

        Returns:
            List[ReportItemTacFarmDashboard]: The Tac Farm Dashboard report.
        """
        report_manager = reports_managers. \
            ReportManagerTacFarmDashboard(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
