# reports/providers/land_plant_list.py
# pylint: disable=unused-import

"""
This module contains the implementation of
the ReportProviderLandPlantList class,
which is responsible for generating a list
of land plants based on the provided parameters.
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


class ReportProviderLandPlantList():
    """
    The ReportProviderLandPlantList
    class is responsible
    for generating a list of land plants
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
        ReportProviderLandPlantList class.

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
        flavor_code: uuid.UUID,
        some_int_val: int,
        some_big_int_val: int,
        some_float_val: float,
        some_bit_val: bool,
        is_edit_allowed: bool,
        is_delete_allowed: bool,
        some_decimal_val: Decimal,
        some_min_utc_date_time_val: datetime,
        some_min_date_val: date,
        some_money_val: Decimal,
        some_n_var_char_val: str,
        some_var_char_val: str,
        some_text_val: str,
        some_phone_number: str,
        some_email_address: str,
        page_number: int,
        item_count_per_page: int,
        order_by_column_name: str,
        order_by_descending: bool,
    ) -> list[dict[str, Any]]:
        """
        Generates a list of land plants based
        on the provided parameters.

        Returns:
            list[dict[str, Any]]: The list of
            land plants as dictionaries.
        """
        flow_name = (
            "ReportProviderLandPlantList"
            ".generate_list"
        )

        logging.info("%s Start", flow_name)
        logging.info("%s context_code: %s", flow_name, str(context_code))
        # offset = (page_number - 1) * item_count_per_page
        query_dict = dict()
        query_dict["context_code"] = (
            str(context_code))
        query_dict["flavor_code"] = (
            str(flavor_code))
        query_dict["some_int_val"] = (
            some_int_val)
        query_dict["some_big_int_val"] = (
            some_big_int_val)
        query_dict["some_float_val"] = (
            some_float_val)
        query_dict["some_bit_val"] = (
            some_bit_val)
        query_dict["is_edit_allowed"] = (
            is_edit_allowed)
        query_dict["is_delete_allowed"] = (
            is_delete_allowed)
        query_dict["some_decimal_val"] = (
            some_decimal_val)
        query_dict["some_min_utc_date_time_val"] = (
            some_min_utc_date_time_val)
        query_dict["some_min_date_val"] = (
            some_min_date_val)
        query_dict["some_money_val"] = (
            some_money_val)
        query_dict["some_n_var_char_val"] = (
            some_n_var_char_val)
        query_dict["some_var_char_val"] = (
            some_var_char_val)
        query_dict["some_text_val"] = (
            some_text_val)
        query_dict["some_phone_number"] = (
            some_phone_number)
        query_dict["some_email_address"] = (
            some_email_address)
        query_dict["like_flavor_code"] = (
            str(flavor_code))
        query_dict["like_some_int_val"] = (
            some_int_val)
        query_dict["like_some_big_int_val"] = (
            some_big_int_val)
        query_dict["like_some_float_val"] = (
            some_float_val)
        query_dict["like_some_bit_val"] = (
            some_bit_val)
        query_dict["like_is_edit_allowed"] = (
            is_edit_allowed)
        query_dict["like_is_delete_allowed"] = (
            is_delete_allowed)
        query_dict["like_some_decimal_val"] = (
            some_decimal_val)
        query_dict["like_some_min_utc_date_time_val"] = (
            some_min_utc_date_time_val)
        query_dict["like_some_min_date_val"] = (
            some_min_date_val)
        query_dict["like_some_money_val"] = (
            some_money_val)
        query_dict["like_some_n_var_char_val"] = (
            '%' + some_n_var_char_val + '%')
        query_dict["like_some_var_char_val"] = (
            '%' + some_var_char_val + '%')
        query_dict["like_some_text_val"] = (
            '%' + some_text_val + '%')
        query_dict["like_some_phone_number"] = (
            '%' + some_phone_number + '%')
        query_dict["like_some_email_address"] = (
            '%' + some_email_address + '%')
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

        if ReportProviderLandPlantList \
                ._cached_sql_query == "":

            sql_folder = "sql_server"
            db_engine_url = str(self._session_context.session.bind.engine.url)
            if 'sqlite' in db_engine_url:
                sql_folder = "sqlite"
            if 'postgresql' in db_engine_url:
                sql_folder = "postgres"
            # Prioritize
            # 'land_plant_list.inc.sql'
            # if it exists
            inc_file_path = (
                f"reports/providers/sql/{sql_folder}/"
                "land_plant_list.inc.sql"
            )
            gen_file_path = (
                f"reports/providers/sql/{sql_folder}/"
                "land_plant_list.gen.sql"
            )
            if os.path.exists(inc_file_path):
                file_to_read = inc_file_path
            elif os.path.exists(gen_file_path):
                file_to_read = gen_file_path
            else:
                raise FileNotFoundError("SQL file not found")

            with open(file_to_read, 'r', encoding='utf-8') as file:
                (ReportProviderLandPlantList
                 ._cached_sql_query) = file.read()

        # Execute the SQL query with the provided parameters
        cursor = await self._session_context.session.execute(
            text(ReportProviderLandPlantList
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
