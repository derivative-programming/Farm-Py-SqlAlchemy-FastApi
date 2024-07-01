

	SELECT * FROM
	(
		SELECT

			dyna_flow_task.code as dyna_flow_task_code,

			dyna_flow_task.is_run_task_debug_required as is_run_task_debug_required,

			0 as run_order,

			dyna_flow.priority_level as dyna_flow_priority_level,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsRunTaskDebugRequired' THEN dyna_flow_task.is_run_task_debug_required  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'RunOrder' THEN 0  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowPriorityLevel' THEN dyna_flow.priority_level  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsRunTaskDebugRequired' THEN dyna_flow_task.is_run_task_debug_required  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'RunOrder' THEN 0  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowPriorityLevel' THEN dyna_flow.priority_level  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			--left join farm_dyna_flow_task dyna_flow_task on 1=1

			left join farm_dyna_flow dyna_flow on dyna_flow.pac_id = pac.pac_id  -- up obj join tree

			left join farm_dyna_flow_type dyna_flowdyna_flow_type on dyna_flow.dyna_flow_type_id = dyna_flowdyna_flow_type.dyna_flow_type_id -- join tree hild obj lookup prop

			left join farm_dyna_flow_task dyna_flow_task on dyna_flow_task.dyna_flow_id = dyna_flow.dyna_flow_id  -- up obj join tree

			left join farm_dyna_flow_task_type dyna_flow_taskdyna_flow_task_type on dyna_flow_task.dyna_flow_task_type_id = dyna_flow_taskdyna_flow_task_type.dyna_flow_task_type_id -- join tree hild obj lookup prop


			  
			left join farm_dyna_flow_task dep_task on dyna_flow_task.dependency_dyna_flow_task_id = dep_task.dyna_flow_task_id 
			left join farm_dyna_flow dep_flow on dyna_flow.dependency_dyna_flow_id = dep_flow.dyna_flow_id  
			left join
			(
				select distinct(dft_dep.dyna_flow_task_id) as locked_task_id
				from
				farm_dft_dependency dft_dep  
				join farm_dyna_flow_task dep_dft on dft_dep.dependency_df_task_id = dep_dft.dyna_flow_task_id and 
				(dep_dft.is_canceled = 0 and dep_dft.is_successful = 0)
			) locked_tasks on locked_tasks.locked_task_id = dyna_flow_task.dyna_flow_task_id 
			

		where
			 (pac.code = :context_code
			   )

				--TriStateFilter IsRunTaskDebugRequiredTriStateFilterCode @IsRunTaskDebugRequiredTriStateFilterCode_TriStateFilterValue
			and (
				:is_run_task_debug_required_tri_state_filter_code is null or
				:is_run_task_debug_required_tri_state_filter_code = '00000000-0000-0000-0000-000000000000' or
				(
					(
						select
							state_int_value
						from
							farm_tri_state_filter
						where code = :is_run_task_debug_required_tri_state_filter_code
					) in (
					-1,
					dyna_flow_task.is_run_task_debug_required
					)
				)
			)
			
		and dyna_flow_task.is_canceled = 0 and
		dyna_flow_task.is_started = 0 and 
		dyna_flow_task.is_completed = 0 and 
		dyna_flow_task.min_start_utc_date_time <= datetime('now') and
		((isnull(dep_task.is_completed,1) = 1 and isnull(dep_task.is_successful,1) = 1) or isnull(dep_task.is_canceled,1) = 1) and
		((isnull(dep_flow.is_completed,1) = 1 and isnull(dep_flow.is_successful,1) = 1) or isnull(dep_flow.is_canceled,1) = 1) and 
		locked_tasks.locked_task_id is null
		 
		    

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

