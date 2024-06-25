# reports/providers/pac_user_tri_state_filter_list.py
# pylint: disable=unused-import

"""
This module contains the implementation of
the ReportProviderPacUserTriStateFilterList class,
which is responsible for generating a list
of pac tri_state_filters based on the provided parameters.
"""

import json
from datetime import date, datetime  # noqa: F401
import os
from typing import Any
import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from helpers import SessionContext


class ReportProviderPacUserTriStateFilterList():
    """
    The ReportProviderPacUserTriStateFilterList
    class is responsible
    for generating a list of pac tri_state_filters
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
        ReportProviderPacUserTriStateFilterList class.

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
        Generates a list of pac tri_state_filters based
        on the provided parameters.

        Returns:
            list[dict[str, Any]]: The list of
            pac tri_state_filters as dictionaries.
        """
        flow_name = (
            "ReportProviderPacUserTriStateFilterList"
            ".generate_list"
        )

        logging.info("%s Start", flow_name)
        logging.info("%s context_code: %s", flow_name, str(context_code))
        # offset = (page_number - 1) * item_count_per_page
        query_dict = dict()
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

        if ReportProviderPacUserTriStateFilterList._cached_sql_query == "":
            # Prioritize 'pac_user_tri_state_filter_list.inc.sql' if it exists
            inc_file_path = "reports/providers/sql/pac_user_tri_state_filter_list.inc.sql"
            gen_file_path = "reports/providers/sql/pac_user_tri_state_filter_list.gen.sql"

            if os.path.exists(inc_file_path):
                file_to_read = inc_file_path
            elif os.path.exists(gen_file_path):
                file_to_read = gen_file_path
            else:
                raise FileNotFoundError("SQL file not found")

            with open(file_to_read, 'r', encoding='utf-8') as file:
                ReportProviderPacUserTriStateFilterList._cached_sql_query = file.read()

        # Execute the SQL query with the provided parameters
        cursor = await self._session_context.session.execute(
            text(ReportProviderPacUserTriStateFilterList._cached_sql_query),
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

