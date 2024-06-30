

	SELECT * FROM
	(
		SELECT

			dyna_flow_type.code as dyna_flow_type_code,

			dyna_flow_type.description as dyna_flow_type_description,

			dyna_flow_type.display_order as dyna_flow_type_display_order,

			dyna_flow_type.is_active as dyna_flow_type_is_active,

			dyna_flow_type.lookup_enum_name as dyna_flow_type_lookup_enum_name,

			dyna_flow_type.name as dyna_flow_type_name,

			dyna_flow_type.priority_level as dyna_flow_type_priority_level,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTypeDescription' THEN dyna_flow_type.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTypeDisplayOrder' THEN dyna_flow_type.display_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTypeIsActive' THEN dyna_flow_type.is_active  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTypeLookupEnumName' THEN dyna_flow_type.lookup_enum_name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTypeName' THEN dyna_flow_type.name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTypePriorityLevel' THEN dyna_flow_type.priority_level  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTypeDescription' THEN dyna_flow_type.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTypeDisplayOrder' THEN dyna_flow_type.display_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTypeIsActive' THEN dyna_flow_type.is_active  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTypeLookupEnumName' THEN dyna_flow_type.lookup_enum_name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTypeName' THEN dyna_flow_type.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTypePriorityLevel' THEN dyna_flow_type.priority_level  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_dyna_flow_type dyna_flow_type on pac.pac_id = dyna_flow_type.pac_id		 --child obj

		where
			 (pac.code = :context_code
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

