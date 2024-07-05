# reports/providers/pac_config_dyna_flow_task_retry_run_list.py
# pylint: disable=unused-import

"""
This module contains the implementation of
the ReportProviderPacConfigDynaFlowTaskRetryRunList class,
which is responsible for generating a list
of pac dyna_flow_tasks based on the provided parameters.
"""

import json
from datetime import date, datetime, timezone  # noqa: F401
import os
from typing import Any
import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from helpers import SessionContext


class ReportProviderPacConfigDynaFlowTaskRetryRunList():
    """
    The ReportProviderPacConfigDynaFlowTaskRetryRunList
    class is responsible
    for generating a list of pac dyna_flow_tasks
    based on the provided parameters.

    Args:
        session_context (SessionContext): The session context object.

    Raises:
        ValueError: If the session is not provided.

    Attributes:
        _session_context (SessionContext): The session context object.
        _session (AsyncSession): The async session object.
        _cached_sql_query (str): Static variable for caching the SQL query.
    """

    _session_context: SessionContext
    _session: AsyncSession
    _cached_sql_query: str = ""

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        ReportProviderPacConfigDynaFlowTaskRetryRunList class.

        Args:
            session_context (SessionContext): The session context object.

        Raises:
            ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context

    async def generate_list(
        self,
        context_code: uuid.UUID,

        page_number: int,
        item_count_per_page: int,
        order_by_column_name: str,
        order_by_descending: bool,
    ) -> list[dict[str, Any]]:
        """
        Generates a list of pac dyna_flow_tasks based
        on the provided parameters.

        Returns:
            list[dict[str, Any]]: The list of
            pac dyna_flow_tasks as dictionaries.
        """
        flow_name = (
            "ReportProviderPacConfigDynaFlowTaskRetryRunList"
            ".generate_list"
        )

        logging.info("%s Start", flow_name)
        logging.info("%s context_code: %s", flow_name, str(context_code))
        # offset = (page_number - 1) * item_count_per_page
        query_dict = {}
        query_dict["context_code"] = (
            str(context_code))


        query_dict["page_number"] = (
            page_number)
        query_dict["item_count_per_page"] = (
            item_count_per_page)
        query_dict["order_by_column_name"] = (
            order_by_column_name)
        query_dict["order_by_descending"] = (
            order_by_descending)
        query_dict["user_id"] = (
            str(self._session_context.customer_code))

        if ReportProviderPacConfigDynaFlowTaskRetryRunList \
                ._cached_sql_query == "":

            sql_folder = "sql_server"
            db_engine_url = str(self._session_context.session.bind.engine.url)
            if 'sqlite' in db_engine_url:
                sql_folder = "sqlite"
            if 'postgresql' in db_engine_url:
                sql_folder = "postgres"
            # Prioritize
            # 'pac_config_dyna_flow_task_retry_run_list.inc.sql'
            # if it exists
            inc_file_path = (
                f"reports/providers/sql/{sql_folder}/"
                "pac_config_dyna_flow_task_retry_run_list.inc.sql"
            )
            gen_file_path = (
                f"reports/providers/sql/{sql_folder}/"
                "pac_config_dyna_flow_task_retry_run_list.gen.sql"
            )
            if os.path.exists(inc_file_path):
                file_to_read = inc_file_path
            elif os.path.exists(gen_file_path):
                file_to_read = gen_file_path
            else:
                raise FileNotFoundError("SQL file not found")

            with open(file_to_read, 'r', encoding='utf-8') as file:
                (ReportProviderPacConfigDynaFlowTaskRetryRunList
                 ._cached_sql_query) = file.read()

        # Execute the SQL query with the provided parameters
        cursor = await self._session_context.session.execute(
            text(ReportProviderPacConfigDynaFlowTaskRetryRunList
                 ._cached_sql_query),
            query_dict
        )

        results = self.dictfetchall(cursor)
        logging.info(
            "%s Results: %s", flow_name, json.dumps(results))
        logging.info("%s End", flow_name)
        return results

    def dictfetchall(self, cursor) -> list[dict[str, Any]]:
        """
        Returns all rows from a cursor as a list of dictionaries.

        Args:
            cursor: The cursor object.

        Returns:
            list[dict[str, Any]]: The list of dictionaries
            representing the rows.
        """
        columns = cursor.keys()
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
