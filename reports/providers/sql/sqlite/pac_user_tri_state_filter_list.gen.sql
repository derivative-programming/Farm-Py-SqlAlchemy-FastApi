

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

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TriStateFilterDescription' THEN tri_state_filter.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TriStateFilterDisplayOrder' THEN tri_state_filter.display_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TriStateFilterIsActive' THEN tri_state_filter.is_active  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TriStateFilterLookupEnumName' THEN tri_state_filter.lookup_enum_name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TriStateFilterName' THEN tri_state_filter.name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TriStateFilterStateIntValue' THEN tri_state_filter.state_int_value  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TriStateFilterDescription' THEN tri_state_filter.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TriStateFilterDisplayOrder' THEN tri_state_filter.display_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TriStateFilterIsActive' THEN tri_state_filter.is_active  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TriStateFilterLookupEnumName' THEN tri_state_filter.lookup_enum_name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TriStateFilterName' THEN tri_state_filter.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TriStateFilterStateIntValue' THEN tri_state_filter.state_int_value  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER

		from
		 	farm_pac  pac  /* owner obj */

			  join farm_tri_state_filter tri_state_filter on pac.pac_id = tri_state_filter.pac_id		 /* child obj*/

		where
			 (pac.code = REPLACE(:context_code, '-', '')
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

