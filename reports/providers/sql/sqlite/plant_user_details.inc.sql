

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

			(select code from farm_tac where lookup_enum_name = 'Primary') as back_to_dashboard_link_tac_code,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER 
		from
		 	farm_plant  plant  

			left join farm_flavor plantFlavor on plant.flvr_foreign_key_id = plantFlavor.flavor_id  

			left join farm_land land on land.land_id = plant.land_id   

			left join farm_pac pac on pac.pac_id = land.pac_id   

		where
			 (plant.code = REPLACE(:context_code, '-', '')
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

