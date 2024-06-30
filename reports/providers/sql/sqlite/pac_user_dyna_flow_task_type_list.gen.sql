

	SELECT * FROM
	(
		SELECT

			dyna_flow_task_type.code as dyna_flow_task_type_code,

			dyna_flow_task_type.description as dyna_flow_task_type_description,

			dyna_flow_task_type.display_order as dyna_flow_task_type_display_order,

			dyna_flow_task_type.is_active as dyna_flow_task_type_is_active,

			dyna_flow_task_type.lookup_enum_name as dyna_flow_task_type_lookup_enum_name,

			dyna_flow_task_type.max_retry_count as dyna_flow_task_type_max_retry_count,

			dyna_flow_task_type.name as dyna_flow_task_type_name,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTaskTypeDescription' THEN dyna_flow_task_type.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTaskTypeDisplayOrder' THEN dyna_flow_task_type.display_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTaskTypeIsActive' THEN dyna_flow_task_type.is_active  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTaskTypeLookupEnumName' THEN dyna_flow_task_type.lookup_enum_name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTaskTypeMaxRetryCount' THEN dyna_flow_task_type.max_retry_count  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTaskTypeName' THEN dyna_flow_task_type.name  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTaskTypeDescription' THEN dyna_flow_task_type.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTaskTypeDisplayOrder' THEN dyna_flow_task_type.display_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTaskTypeIsActive' THEN dyna_flow_task_type.is_active  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTaskTypeLookupEnumName' THEN dyna_flow_task_type.lookup_enum_name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTaskTypeMaxRetryCount' THEN dyna_flow_task_type.max_retry_count  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTaskTypeName' THEN dyna_flow_task_type.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_dyna_flow_task_type dyna_flow_task_type on pac.pac_id = dyna_flow_task_type.pac_id		 --child obj

		where
			 (pac.code = :context_code
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

