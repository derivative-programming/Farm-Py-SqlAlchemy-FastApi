# business/tac.py
# pylint: disable=unused-import
"""
"""
import uuid
from decimal import Decimal  # noqa: F401
from datetime import date, datetime  # noqa: F401
from typing import List
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Tac
import models
import managers as managers_and_enums  # noqa: F401
from .tac_fluent import TacFluentBusObj
import reports as reports_managers  # noqa: F401


class TacReportsBusObj(TacFluentBusObj):
    """
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
