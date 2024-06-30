

	SELECT * FROM
	(
		SELECT

			date_greater_than_filter.code as date_greater_than_filter_code,

			date_greater_than_filter.day_count as date_greater_than_filter_day_count,

			date_greater_than_filter.description as date_greater_than_filter_description,

			date_greater_than_filter.display_order as date_greater_than_filter_display_order,

			date_greater_than_filter.is_active as date_greater_than_filter_is_active,

			date_greater_than_filter.lookup_enum_name as date_greater_than_filter_lookup_enum_name,

			date_greater_than_filter.name as date_greater_than_filter_name,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DateGreaterThanFilterDayCount' THEN date_greater_than_filter.day_count  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DateGreaterThanFilterDescription' THEN date_greater_than_filter.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DateGreaterThanFilterDisplayOrder' THEN date_greater_than_filter.display_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DateGreaterThanFilterIsActive' THEN date_greater_than_filter.is_active  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DateGreaterThanFilterLookupEnumName' THEN date_greater_than_filter.lookup_enum_name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DateGreaterThanFilterName' THEN date_greater_than_filter.name  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DateGreaterThanFilterDayCount' THEN date_greater_than_filter.day_count  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DateGreaterThanFilterDescription' THEN date_greater_than_filter.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DateGreaterThanFilterDisplayOrder' THEN date_greater_than_filter.display_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DateGreaterThanFilterIsActive' THEN date_greater_than_filter.is_active  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DateGreaterThanFilterLookupEnumName' THEN date_greater_than_filter.lookup_enum_name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DateGreaterThanFilterName' THEN date_greater_than_filter.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_date_greater_than_filter date_greater_than_filter on pac.pac_id = date_greater_than_filter.pac_id		 --child obj

		where
			 (pac.code = :context_code
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

