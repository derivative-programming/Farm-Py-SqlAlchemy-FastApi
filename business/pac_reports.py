# business/pac_reports.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the PacReportsBusObj class
which provides methods to generate various reports
related to Pac objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Pac

from .pac_fluent import PacFluentBusObj


class PacReportsBusObj(PacFluentBusObj):
    """
    This class extends the PacFluentBusObj class
    and provides methods to generate various reports
    related to Pac objects.
    """


    async def generate_report_pac_user_tri_state_filter_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacUserTriStateFilterList]:
        """
        Get the Pac User Tri State Filter List report.

        Returns:
            List[ReportItemPacUserTriStateFilterList]:
                The Pac User Tri State Filter List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacUserTriStateFilterList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_user_tac_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacUserTacList]:
        """
        Get the Pac User Tac List report.

        Returns:
            List[ReportItemPacUserTacList]:
                The Pac User Tac List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacUserTacList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_user_role_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacUserRoleList]:
        """
        Get the Pac User Role List report.

        Returns:
            List[ReportItemPacUserRoleList]:
                The Pac User Role List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacUserRoleList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_user_land_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacUserLandList]:
        """
        Get the Pac User Land List report.

        Returns:
            List[ReportItemPacUserLandList]:
                The Pac User Land List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacUserLandList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_user_flavor_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacUserFlavorList]:
        """
        Get the Pac User Flavor List report.

        Returns:
            List[ReportItemPacUserFlavorList]:
                The Pac User Flavor List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacUserFlavorList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_user_dyna_flow_type_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacUserDynaFlowTypeList]:
        """
        Get the Pac User Dyna Flow Type List report.

        Returns:
            List[ReportItemPacUserDynaFlowTypeList]:
                The Pac User Dyna Flow Type List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacUserDynaFlowTypeList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_user_dyna_flow_task_type_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacUserDynaFlowTaskTypeList]:
        """
        Get the Pac User Dyna Flow Task Type List report.

        Returns:
            List[ReportItemPacUserDynaFlowTaskTypeList]:
                The Pac User Dyna Flow Task Type List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacUserDynaFlowTaskTypeList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_user_date_greater_than_filter_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacUserDateGreaterThanFilterList]:
        """
        Get the Pac User Date Greater Than Filter List report.

        Returns:
            List[ReportItemPacUserDateGreaterThanFilterList]:
                The Pac User Date Greater Than Filter List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacUserDateGreaterThanFilterList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_config_dyna_flow_task_search(
        self,
        started_date_greater_than_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        processor_identifier:
            str = "",
        is_started_tri_state_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        is_completed_tri_state_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        is_successful_tri_state_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacConfigDynaFlowTaskSearch]:
        """
        Get the Pac Config Dyna Flow Task Search report.

        Returns:
            List[ReportItemPacConfigDynaFlowTaskSearch]:
                The Pac Config Dyna Flow Task Search report.
        """
        report_manager = reports_managers. \
            ReportManagerPacConfigDynaFlowTaskSearch(
                self._session_context)
        return await report_manager.generate(
            self.code,
            started_date_greater_than_filter_code,
            processor_identifier,
            is_started_tri_state_filter_code,
            is_completed_tri_state_filter_code,
            is_successful_tri_state_filter_code,
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_config_dyna_flow_task_run_to_do_list(
        self,
        is_run_task_debug_required_tri_state_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacConfigDynaFlowTaskRunToDoList]:
        """
        Get the Pac Config Dyna Flow Task Run To Do List report.

        Returns:
            List[ReportItemPacConfigDynaFlowTaskRunToDoList]:
                The Pac Config Dyna Flow Task Run To Do List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacConfigDynaFlowTaskRunToDoList(
                self._session_context)
        return await report_manager.generate(
            self.code,
            is_run_task_debug_required_tri_state_filter_code,
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_config_dyna_flow_task_retry_run_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacConfigDynaFlowTaskRetryRunList]:
        """
        Get the Pac Config Dyna Flow Task Retry Run List report.

        Returns:
            List[ReportItemPacConfigDynaFlowTaskRetryRunList]:
                The Pac Config Dyna Flow Task Retry Run List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacConfigDynaFlowTaskRetryRunList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_config_dyna_flow_retry_task_build_list(
        self,

        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacConfigDynaFlowRetryTaskBuildList]:
        """
        Get the Pac Config Dyna Flow Retry Task Build List report.

        Returns:
            List[ReportItemPacConfigDynaFlowRetryTaskBuildList]:
                The Pac Config Dyna Flow Retry Task Build List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacConfigDynaFlowRetryTaskBuildList(
                self._session_context)
        return await report_manager.generate(
            self.code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )


    async def generate_report_pac_config_dyna_flow_dft_build_to_do_list(
        self,
        is_build_task_debug_required_tri_state_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemPacConfigDynaFlowDFTBuildToDoList]:
        """
        Get the Pac Config Dyna Flow DFT Build To Do List report.

        Returns:
            List[ReportItemPacConfigDynaFlowDFTBuildToDoList]:
                The Pac Config Dyna Flow DFT Build To Do List report.
        """
        report_manager = reports_managers. \
            ReportManagerPacConfigDynaFlowDFTBuildToDoList(
                self._session_context)
        return await report_manager.generate(
            self.code,
            is_build_task_debug_required_tri_state_filter_code,
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
