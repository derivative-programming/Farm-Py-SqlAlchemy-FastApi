

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

			pac.code as test_file_download_link_pac_code,

			pac.code as test_conditional_file_download_link_pac_code,

			pac.code as test_async_flow_req_link_pac_code,

			pac.code as test_conditional_async_flow_req_link_pac_code,

			plant.code as conditional_btn_example_link_plant_code,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeIntVal' THEN plant.some_int_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeBigIntVal' THEN plant.some_big_int_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeBitVal' THEN plant.some_bit_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsEditAllowed' THEN plant.is_edit_allowed  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsDeleteAllowed' THEN plant.is_delete_allowed  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeFloatVal' THEN plant.some_float_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeDecimalVal' THEN plant.some_decimal_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeUTCDateTimeVal' THEN plant.some_utc_date_time_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeDateVal' THEN plant.some_date_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeMoneyVal' THEN plant.some_money_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeNVarCharVal' THEN plant.some_n_var_char_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeVarCharVal' THEN plant.some_var_char_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomePhoneNumber' THEN plant.some_phone_number  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeEmailAddress' THEN plant.some_email_address  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'FlavorName' THEN plantflavor.name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'SomeIntConditionalOnDeletable' THEN plant.some_int_val  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'NVarCharAsUrl' THEN plant.some_n_var_char_val  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeIntVal' THEN plant.some_int_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeBigIntVal' THEN plant.some_big_int_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeBitVal' THEN plant.some_bit_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsEditAllowed' THEN plant.is_edit_allowed  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsDeleteAllowed' THEN plant.is_delete_allowed  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeFloatVal' THEN plant.some_float_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeDecimalVal' THEN plant.some_decimal_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeUTCDateTimeVal' THEN plant.some_utc_date_time_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeDateVal' THEN plant.some_date_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeMoneyVal' THEN plant.some_money_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeNVarCharVal' THEN plant.some_n_var_char_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeVarCharVal' THEN plant.some_var_char_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomePhoneNumber' THEN plant.some_phone_number  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeEmailAddress' THEN plant.some_email_address  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'FlavorName' THEN plantflavor.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'SomeIntConditionalOnDeletable' THEN plant.some_int_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'NVarCharAsUrl' THEN plant.some_n_var_char_val  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER

		from
		 	farm_land  land  /* owner obj */

			  join farm_plant plant on land.land_id = plant.land_id		 /* child obj*/

			left join farm_flavor plantflavor on plant.flvr_foreign_key_id = plantflavor.flavor_id /* child obj lookup prop*/

			left join farm_pac pac on pac.pac_id = land.pac_id  /*  up obj tree*/

		where
			 (land.code = REPLACE(:context_code, '-', '')
			   )

			and (:some_n_var_char_val is null or :some_n_var_char_val = '' or  plant.some_n_var_char_val like :like_some_n_var_char_val)

			and (:some_var_char_val is null or :some_var_char_val = '' or  plant.some_var_char_val like :like_some_var_char_val)

			and (:some_text_val is null or :some_text_val = '' or  plant.some_text_val like :like_some_text_val)

			and (:some_phone_number is null or :some_phone_number = '' or  plant.some_phone_number like :like_some_phone_number)

			and (:some_email_address is null or :some_email_address = '' or  plant.some_email_address like :like_some_email_address)

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

