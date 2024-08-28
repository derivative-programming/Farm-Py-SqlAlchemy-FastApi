

	SELECT * FROM
	(
		SELECT

			land.code as field_one_plant_list_link_land_code,

			land.code as conditional_btn_example_link_land_code,

			cast((case when 1=0 then 1 else 0 end) as bit) as is_conditional_btn_available,

			pac.code as test_file_download_link_pac_code,

			pac.code as test_conditional_file_download_link_pac_code,

			pac.code as test_async_flow_req_link_pac_code,

			pac.code as test_conditional_async_flow_req_link_pac_code,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER

		from
		 	farm_tac  tac  /* owner obj */

			left join farm_pac pac on pac.pac_id = tac.pac_id  /*  up obj tree*/

		where
			 (tac.code = REPLACE(:context_code, '-', '')
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

