import json
from datetime import date, datetime
import uuid
from decimal import Decimal
import logging
from helpers import SessionContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
class ReportProviderTacFarmDashboard():
		_session_context:SessionContext
		_session:AsyncSession
		def __init__(self, session:AsyncSession, session_context:SessionContext):
			self._session = session
			self._session_context = session_context
		async def generate_list(
			self,
			context_code:uuid,

			page_number:int,
			item_count_per_page:int,
			order_by_column_name:str,
			order_by_descending:bool,
		) -> list[dict[str,any]]:
			logging.info("ReportProviderTacFarmDashboard.generate_list Start")
			logging.info("ReportProviderTacFarmDashboard.generate_list context_code:" + str(context_code))
			offset = (page_number - 1) * item_count_per_page
			query_dict = dict()
			query_dict["context_code"] = str(context_code)

			query_dict["page_number"] = page_number
			query_dict["item_count_per_page"] = item_count_per_page
			query_dict["order_by_column_name"] = order_by_column_name
			query_dict["order_by_descending"] = order_by_descending
			query_dict["user_id"] = str(self._session_context.customer_code)
			# The hardcoded path to the SQL file in the 'sql' subfolder
			file_path = "reports/providers/sql/tac_farm_dashboard.gen.sql"
			# Read SQL from the hardcoded file path
			with open(file_path, 'r') as file:
				sql_query = file.read()
			# Execute the SQL query with the provided parameters
			cursor = await self._session.execute(
				text(sql_query),
				query_dict
			)
			results = self.dictfetchall(cursor)
			logging.info("ReportProviderTacFarmDashboard.generate_list Results: " + json.dumps(results))
			logging.info("ReportProviderTacFarmDashboard.generate_list End")
			return results
		def dictfetchall(self, cursor) -> list[dict[str,any]]:
			"Return all rows from a cursor as a dict"
			# columns = [col[0] for col in cursor.description]
			# Get the column names from the CursorResult object
			columns = cursor.keys()
			return [
				dict(zip(columns, row))
				for row in cursor.fetchall()
			]

