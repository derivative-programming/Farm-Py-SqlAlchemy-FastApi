# tac_farm_dashboard.py
"""
    #TODO add comment
"""
import json
from datetime import date, datetime
import os
import uuid
from decimal import Decimal
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from helpers import SessionContext
class ReportProviderTacFarmDashboard():
    """
    #TODO add comment
    """
    _session_context: SessionContext
    _session: AsyncSession
    _cached_sql_query: str = None  # Static variable for caching the SQL query
    def __init__(self, session_context: SessionContext):
        """
            #TODO add comment
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
    ) -> list[dict[str, any]]:
        """
            #TODO add comment
        """
        flow_name = "ReportProviderTacFarmDashboard.generate_list"
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
        if ReportProviderTacFarmDashboard._cached_sql_query is None:
            # Prioritize 'tac_farm_dashboard.inc.sql' if it exists
            inc_file_path = "reports/providers/sql/tac_farm_dashboard.inc.sql"
            gen_file_path = "reports/providers/sql/tac_farm_dashboard.gen.sql"
            if os.path.exists(inc_file_path):
                file_to_read = inc_file_path
            elif os.path.exists(gen_file_path):
                file_to_read = gen_file_path
            else:
                raise FileNotFoundError("SQL file not found")
            with open(file_to_read, 'r') as file:
                ReportProviderTacFarmDashboard._cached_sql_query = file.read()
        # Execute the SQL query with the provided parameters
        cursor = await self._session_context.session.execute(
            text(ReportProviderTacFarmDashboard._cached_sql_query),
            query_dict
        )
        results = self.dictfetchall(cursor)
        logging.info(
            "%s Results: %s", flow_name, json.dumps(results))
        logging.info("%s End", flow_name)
        return results
    def dictfetchall(self, cursor) -> list[dict[str, any]]:
        "Return all rows from a cursor as a dict"
        # columns = [col[0] for col in cursor.description]
        # Get the column names from the CursorResult object
        columns = cursor.keys()
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

