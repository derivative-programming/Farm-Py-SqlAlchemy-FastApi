import json
from datetime import date, datetime
import uuid
from decimal import Decimal 
from reports.row_models import ReportItemLandPlantList
import logging
from helpers import SessionContext
class ReportProviderLandPlantList():
    _session_context:SessionContext
    def __init__(self, session_context:SessionContext):
        self._session_context = session_context
    def generate_list(self,
                    context_code:uuid,
                    flavor_code: uuid,
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
                    page_number:int,
                    item_count_per_page:int,
                    order_by_column_name:str,
                    order_by_descending:bool,
                      ) -> list[dict[str,any]]:
        logging.debug("ReportProviderLandPlantList.generate_list Start")
        logging.debug("ReportProviderLandPlantList.generate_list context_code:" + str(context_code))
        offset = (page_number - 1) * item_count_per_page
        query_dict = dict()
        query_dict["context_code"] = str(context_code)
        query_dict["flavor_code"] = str(flavor_code)
        query_dict["some_int_val"] = some_int_val
        query_dict["some_big_int_val"] = some_big_int_val
        query_dict["some_float_val"] = some_float_val
        query_dict["some_bit_val"] = some_bit_val
        query_dict["is_edit_allowed"] = is_edit_allowed
        query_dict["is_delete_allowed"] = is_delete_allowed
        query_dict["some_decimal_val"] = some_decimal_val
        query_dict["some_min_utc_date_time_val"] = some_min_utc_date_time_val
        query_dict["some_min_date_val"] = some_min_date_val
        query_dict["some_money_val"] = some_money_val
        query_dict["some_n_var_char_val"] = some_n_var_char_val
        query_dict["some_var_char_val"] = some_var_char_val
        query_dict["some_text_val"] = some_text_val
        query_dict["some_phone_number"] = some_phone_number
        query_dict["some_email_address"] = some_email_address

        query_dict["like_flavor_code"] = str(flavor_code)
        query_dict["like_some_int_val"] = some_int_val
        query_dict["like_some_big_int_val"] = some_big_int_val
        query_dict["like_some_float_val"] = some_float_val
        query_dict["like_some_bit_val"] = some_bit_val
        query_dict["like_is_edit_allowed"] = is_edit_allowed
        query_dict["like_is_delete_allowed"] = is_delete_allowed
        query_dict["like_some_decimal_val"] = some_decimal_val
        query_dict["like_some_min_utc_date_time_val"] = some_min_utc_date_time_val
        query_dict["like_some_min_date_val"] = some_min_date_val
        query_dict["like_some_money_val"] = some_money_val
        query_dict["like_some_n_var_char_val"] = '%' + some_n_var_char_val + '%'
        query_dict["like_some_var_char_val"] = '%' + some_var_char_val  + '%'
        query_dict["like_some_text_val"] = '%' + some_text_val  + '%'
        query_dict["like_some_phone_number"] = '%' + some_phone_number  + '%'
        query_dict["like_some_email_address"] = '%' + some_email_address  + '%'

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

			plant.code as plant_code,

			plant.some_int_val as some_int_val,

			plant.some_big_int_val as some_big_int_val,

			plant.some_bit_val as some_bit_val,

			plant.is_edit_allowed as is_edit_allowed,

			plant.is_delete_allowed as is_delete_allowed,

			plant.some_float_val as some_float_val,

			plant.some_decimal_val as some_decimal_val,

			plant.some_utc_date_time_val as some_utc_date_time_val,

			plant.some_date_val as some_date_val,

			plant.some_money_val as some_money_val,

			plant.some_n_var_char_val as some_n_var_char_val,

			plant.some_var_char_val as some_var_char_val,

			plant.some_text_val as some_text_val,

			plant.some_phone_number as some_phone_number,

			plant.some_email_address as some_email_address,

			plantflavor.name as flavor_name,

			plantflavor.code as flavor_code,

			plant.some_int_val as some_int_conditional_on_deletable,

			plant.some_n_var_char_val as n_var_char_as_url,

			plant.code as update_link_plant_code,

			plant.code as delete_async_button_link_plant_code,

			plant.code as details_link_plant_code,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeIntVal' THEN plant.some_int_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeBigIntVal' THEN plant.some_big_int_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeBitVal' THEN plant.some_bit_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'IsEditAllowed' THEN plant.is_edit_allowed  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'IsDeleteAllowed' THEN plant.is_delete_allowed  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeFloatVal' THEN plant.some_float_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeDecimalVal' THEN plant.some_decimal_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeUTCDateTimeVal' THEN plant.some_utc_date_time_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeDateVal' THEN plant.some_date_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeMoneyVal' THEN plant.some_money_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeNVarCharVal' THEN plant.some_n_var_char_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeVarCharVal' THEN plant.some_var_char_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomePhoneNumber' THEN plant.some_phone_number  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeEmailAddress' THEN plant.some_email_address  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'FlavorName' THEN plantflavor.name  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'SomeIntConditionalOnDeletable' THEN plant.some_int_val  END ASC,

					CASE WHEN %(order_by_descending)s = 0 and %(order_by_column_name)s = 'NVarCharAsUrl' THEN plant.some_n_var_char_val  END ASC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeIntVal' THEN plant.some_int_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeBigIntVal' THEN plant.some_big_int_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeBitVal' THEN plant.some_bit_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'IsEditAllowed' THEN plant.is_edit_allowed  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'IsDeleteAllowed' THEN plant.is_delete_allowed  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeFloatVal' THEN plant.some_float_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeDecimalVal' THEN plant.some_decimal_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeUTCDateTimeVal' THEN plant.some_utc_date_time_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeDateVal' THEN plant.some_date_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeMoneyVal' THEN plant.some_money_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeNVarCharVal' THEN plant.some_n_var_char_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeVarCharVal' THEN plant.some_var_char_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomePhoneNumber' THEN plant.some_phone_number  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeEmailAddress' THEN plant.some_email_address  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'FlavorName' THEN plantflavor.name  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'SomeIntConditionalOnDeletable' THEN plant.some_int_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'NVarCharAsUrl' THEN plant.some_n_var_char_val  END DESC,

					CASE WHEN %(order_by_descending)s = 1 and %(order_by_column_name)s = 'placeholder' THEN ''  END DESC
				) AS ROWNUMBER
		  -- select *
		from
		 	farm_land  land  --owner obj

			  join farm_plant plant on land.land_id = plant.land_id		 --child obj

			left join farm_flavor plantflavor on plant.flvr_foreign_key_id = plantflavor.flavor_id --child obj lookup prop

			left join farm_pac pac on pac.pac_id = land.pac_id  -- up obj tree

		where
			 (land.code = %(context_code)s
			   )

			and (%(flavor_code)s is null or %(flavor_code)s = '00000000-0000-0000-0000-000000000000' or %(flavor_code)s = plantflavor.code)

			and (%(some_int_val)s is null or %(some_int_val)s = 0 or %(some_int_val)s = plant.some_int_val)

			and (%(some_big_int_val)s is null or %(some_big_int_val)s = 0 or %(some_big_int_val)s = plant.some_big_int_val)

			and (%(some_float_val)s is null or %(some_float_val)s = 0 or %(some_float_val)s = plant.some_float_val)

			and (%(some_bit_val)s is null or %(some_bit_val)s = 0 or %(some_bit_val)s = plant.some_bit_val)

			and (%(is_edit_allowed)s is null or %(is_edit_allowed)s = 0 or %(is_edit_allowed)s = plant.is_edit_allowed)

			and (%(is_delete_allowed)s is null or %(is_delete_allowed)s = 0 or %(is_delete_allowed)s = plant.is_edit_allowed)

			and (%(some_decimal_val)s is null or %(some_decimal_val)s = 0 or %(some_decimal_val)s = plant.some_decimal_val)

			and (%(some_min_utc_date_time_val)s is null or %(some_min_utc_date_time_val)s = Null or %(some_min_utc_date_time_val)s = plant.some_utc_date_time_val)

			and (%(some_min_date_val)s is null or %(some_min_date_val)s = Null or %(some_min_date_val)s = plant.some_date_val)

			and (%(some_money_val)s is null or %(some_money_val)s = 0 or %(some_money_val)s = plant.some_money_val)

			and (%(some_n_var_char_val)s is null or %(some_n_var_char_val)s = '' or  plant.some_n_var_char_val like %(like_some_n_var_char_val)s)

			and (%(some_var_char_val)s is null or %(some_var_char_val)s = '' or  plant.some_var_char_val like %(like_some_var_char_val)s)

			and (%(some_text_val)s is null or %(some_text_val)s = '' or  plant.some_text_val like %(like_some_text_val)s)

			and (%(some_phone_number)s is null or %(some_phone_number)s = '' or  plant.some_phone_number like %(like_some_phone_number)s)

			and (%(some_email_address)s is null or %(some_email_address)s = '' or  plant.some_email_address like %(like_some_email_address)s)

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((%(page_number)s - 1) * %(item_count_per_page)s + 1) AND (%(page_number)s * %(item_count_per_page)s)
                """, query_dict)
            results = self.dictfetchall(cursor)
        logging.debug("ReportProviderLandPlantList.generate_list Results: " + json.dumps(results))
        logging.debug("ReportProviderLandPlantList.generate_list End")
        return results
    def dictfetchall(self, cursor) -> list[dict[str,any]]:
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

