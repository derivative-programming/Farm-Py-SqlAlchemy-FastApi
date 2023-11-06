import json
from datetime import date, datetime
import uuid
from decimal import Decimal
from django.db import connection
from farm.reports.row_models import ReportItemPacUserTriStateFilterList
import logging
from farm.helpers import SessionContext
class ReportProviderPacUserTriStateFilterList():
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
        logging.debug("ReportProviderPacUserTriStateFilterList.generate_list Start")
        logging.debug("ReportProviderPacUserTriStateFilterList.generate_list context_code:" + str(context_code))
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

			tri_state_filter.code as tri_state_filter_code,

			tri_state_filter.description as tri_state_filter_description,

			tri_state_filter.display_order as tri_state_filter_display_order,

			tri_state_filter.is_active as tri_state_filter_is_active,

			tri_state_filter.lookup_enum_name as tri_state_filter_lookup_enum_name,

			tri_state_filter.name as tri_state_filter_name,

			tri_state_filter.state_int_value as tri_state_filter_state_int_value,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TriStateFilterDescription' THEN tri_state_filter.description  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TriStateFilterDisplayOrder' THEN tri_state_filter.display_order  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TriStateFilterIsActive' THEN tri_state_filter.is_active  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TriStateFilterLookupEnumName' THEN tri_state_filter.lookup_enum_name  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TriStateFilterName' THEN tri_state_filter.name  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'TriStateFilterStateIntValue' THEN tri_state_filter.state_int_value  END ASC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TriStateFilterDescription' THEN tri_state_filter.description  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TriStateFilterDisplayOrder' THEN tri_state_filter.display_order  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TriStateFilterIsActive' THEN tri_state_filter.is_active  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TriStateFilterLookupEnumName' THEN tri_state_filter.lookup_enum_name  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TriStateFilterName' THEN tri_state_filter.name  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'TriStateFilterStateIntValue' THEN tri_state_filter.state_int_value  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'placeholder' THEN ''  END DESC
				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_tri_state_filter tri_state_filter on pac.pac_id = tri_state_filter.pac_id		 --child obj

		where
			 (pac.code = %(context_code)s
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((%(page_number)s - 1) * %(item_count_per_page)s + 1) AND (%(page_number)s * %(item_count_per_page)s)
                """, query_dict)
            results = self.dictfetchall(cursor)
        logging.debug("ReportProviderPacUserTriStateFilterList.generate_list Results: " + json.dumps(results))
        logging.debug("ReportProviderPacUserTriStateFilterList.generate_list End")
        return results
    def dictfetchall(self, cursor) -> list[dict[str,any]]:
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

