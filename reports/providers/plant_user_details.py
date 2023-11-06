import json
from datetime import date, datetime
import uuid
from decimal import Decimal
from django.db import connection
from farm.reports.row_models import ReportItemPlantUserDetails
import logging
from farm.helpers import SessionContext
class ReportProviderPlantUserDetails():
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
        logging.debug("ReportProviderPlantUserDetails.generate_list Start")
        logging.debug("ReportProviderPlantUserDetails.generate_list context_code:" + str(context_code))
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

			plantflavor.name as flavor_name,

			plant.is_delete_allowed as is_delete_allowed,

			plant.is_edit_allowed as is_edit_allowed,

			plant.other_flavor as other_flavor,

			plant.some_big_int_val as some_big_int_val,

			plant.some_bit_val as some_bit_val,

			plant.some_date_val as some_date_val,

			plant.some_decimal_val as some_decimal_val,

			plant.some_email_address as some_email_address,

			plant.some_float_val as some_float_val,

			plant.some_int_val as some_int_val,

			plant.some_money_val as some_money_val,

			plant.some_n_var_char_val as some_n_var_char_val,

			plant.some_phone_number as some_phone_number,

			plant.some_text_val as some_text_val,

			plant.some_uniqueidentifier_val as some_uniqueidentifier_val,

			plant.some_utc_date_time_val as some_utc_date_time_val,

			plant.some_var_char_val as some_var_char_val,

			plant.some_phone_number as phone_num_conditional_on_is_editable,

			plant.some_n_var_char_val as n_var_char_as_url,

			plant.code as update_button_text_link_plant_code,

			plant.code as random_property_updates_link_plant_code,

			tac.code as back_to_dashboard_link_tac_code,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'placeholder' THEN ''  END DESC
				) AS ROWNUMBER
		  -- select *
		from
		 	farm_plant  plant  --owner obj

			left join farm_flavor plantFlavor on plant.flvr_foreign_key_id = plantFlavor.flavor_id   -- fk prop

			left join farm_land land on land.land_id = plant.land_id  -- up obj tree

			left join farm_pac pac on pac.pac_id = land.pac_id  -- up obj tree

		where
			 (plant.code = %(context_code)s
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((%(page_number)s - 1) * %(item_count_per_page)s + 1) AND (%(page_number)s * %(item_count_per_page)s)
                """, query_dict)
            results = self.dictfetchall(cursor)
        logging.debug("ReportProviderPlantUserDetails.generate_list Results: " + json.dumps(results))
        logging.debug("ReportProviderPlantUserDetails.generate_list End")
        return results
    def dictfetchall(self, cursor) -> list[dict[str,any]]:
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

