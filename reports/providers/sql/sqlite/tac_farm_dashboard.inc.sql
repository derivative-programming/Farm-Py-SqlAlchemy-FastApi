

	SELECT * FROM
	(
		SELECT

			land.code as field_one_plant_list_link_land_code,

			land.code as conditional_btn_example_link_land_code,

			cast((case when 1=0 then 1 else 0 end) as bit) as is_conditional_btn_available,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_land  land  --owner obj 

		where
			 land.lookup_enum_name = 'Field_One' 

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

