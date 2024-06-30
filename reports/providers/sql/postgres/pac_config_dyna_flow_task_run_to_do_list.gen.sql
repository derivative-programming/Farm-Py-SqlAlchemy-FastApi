

		--TriStateFilter IsRunTaskDebugRequiredTriStateFilterCode
		DECLARE @IsRunTaskDebugRequiredTriStateFilterCode_TriStateFilterValue int = -1
		select @IsRunTaskDebugRequiredTriStateFilterCode_TriStateFilterValue = StateIntValue from TriStateFilter where code = :is_run_task_debug_required_tri_state_filter_code

	SELECT * FROM
	(
		SELECT

			dyna_flow_task.code as dyna_flow_task_code,

			dyna_flow_task.is_run_task_debug_required as is_run_task_debug_required,

			pac.run_order as run_order,

			dyna_flow.priority_level as dyna_flow_priority_level,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsRunTaskDebugRequired' THEN dyna_flow_task.is_run_task_debug_required  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'RunOrder' THEN pac.run_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowPriorityLevel' THEN dyna_flow.priority_level  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsRunTaskDebugRequired' THEN dyna_flow_task.is_run_task_debug_required  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'RunOrder' THEN pac.run_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowPriorityLevel' THEN dyna_flow.priority_level  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			--left join farm_dyna_flow_task dyna_flow_task on 1=1

			left join farm_dyna_flow dyna_flow on dyna_flow.pac_id = pac.pac_id  -- up obj join tree

			left join farm_dyna_flow_type dyna_flowdyna_flow_type on dyna_flow.dyna_flow_type_id = dyna_flowDynaFlowType.dyna_flow_type_id -- join tree hild obj lookup prop

			left join farm_dyna_flow_task dyna_flow_task on dyna_flow_task.dyna_flow_id = dyna_flow.dyna_flow_id  -- up obj join tree

			left join farm_dyna_flow_task_type dyna_flow_taskdyna_flow_task_type on dyna_flow_task.dyna_flow_task_type_id = dyna_flow_taskDynaFlowTaskType.dyna_flow_task_type_id -- join tree hild obj lookup prop

		where
			 (pac.code = :context_code
			   )

				--TriStateFilter IsRunTaskDebugRequiredTriStateFilterCode @IsRunTaskDebugRequiredTriStateFilterCode_TriStateFilterValue
			and (:is_run_task_debug_required_tri_state_filter_code is null or :is_run_task_debug_required_tri_state_filter_code = '00000000-0000-0000-0000-000000000000' or @IsRunTaskDebugRequiredTriStateFilterCode_TriStateFilterValue = -1 or @IsRunTaskDebugRequiredTriStateFilterCode_TriStateFilterValue = dyna_flow_task.is_run_task_debug_required)

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

