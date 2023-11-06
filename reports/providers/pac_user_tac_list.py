import json
from datetime import date, datetime
import uuid
from decimal import Decimal
from django.db import connection
from farm.reports.row_models import ReportItemPacUserTacList
import logging
from farm.helpers import SessionContext
class ReportProviderPacUserTacList():
    _session_context:SessionContext
    def __init__(self, session_context:SessionContext):
        self._session_context = session_context
    def generate_list(self,
                    context_code:uuid,

                    page_number:int,
                    item_count_per_page:int,
                    order_by_column_name:str,
                    order_by_descending:bool,
                      ) -> list[dict[str,any]]:
        logging.debug("ReportProviderPacUserTacList.generate_list Start")
        logging.debug("ReportProviderPacUserTacList.generate_list context_code:" + str(context_code))
        offset = (page_number - 1) * item_count_per_page
        query_dict = dict()
        query_dict["context_code"] = str(context_code)

        query_dict["page_number"] = page_number
        query_dict["item_count_per_page"] = item_count_per_page
        query_dict["order_by_column_name"] = order_by_column_name
        query_dict["order_by_descending"] = order_by_descending
        query_dict["user_id"] = str(self._session_context.customer_code)
        results = list()
        with connection.cursor() as cursor:
            cursor.execute("""

	SELECT * FROM
	(
		SELECT

			tac.code as tac_code,

			tac.description as tac_description,

			tac.display_order as tac_display_order,

			tac.is_active as tac_is_active,

			tac.lookup_enum_name as tac_lookup_enum_name,

			tac.name as tac_name,

			pac.name as pac_name,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TacDescription' THEN tac.description  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TacDisplayOrder' THEN tac.display_order  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TacIsActive' THEN tac.is_active  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TacLookupEnumName' THEN tac.lookup_enum_name  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TacName' THEN tac.name  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'PacName' THEN pac.name  END ASC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TacDescription' THEN tac.description  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TacDisplayOrder' THEN tac.display_order  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TacIsActive' THEN tac.is_active  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TacLookupEnumName' THEN tac.lookup_enum_name  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TacName' THEN tac.name  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'PacName' THEN pac.name  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'placeholder' THEN ''  END DESC
				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_tac tac on pac.pac_id = tac.pac_id		 --child obj

		where
			 (pac.code = %(context_code)s
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((%(page_number)s - 1) * %(item_count_per_page)s + 1) AND (%(page_number)s * %(item_count_per_page)s)
                """, query_dict)
            results = self.dictfetchall(cursor)
        logging.debug("ReportProviderPacUserTacList.generate_list Results: " + json.dumps(results))
        logging.debug("ReportProviderPacUserTacList.generate_list End")
        return results
    def dictfetchall(self, cursor) -> list[dict[str,any]]:
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

