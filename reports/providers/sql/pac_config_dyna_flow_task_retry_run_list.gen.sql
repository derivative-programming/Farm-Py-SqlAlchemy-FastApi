

	SELECT * FROM
	(
		SELECT

			dyna_flow_task.code as dyna_flow_task_code,

			ROW_NUMBER() OVER(
				ORDER BY

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
			 And DynaFlowTask.IsSuccessful = 0 and DynaFlowTask.IsCanceled = 0 and DynaFlowTask.IsStarted = 1 and DynaFlowTask.RequestedUTCDateTime > dateadd(HOUR,-24,getutcdate()) and DynaFlowTask.StartedUTCDateTime < dateadd(HOUR,-2,getutcdate()) and not (DynaFlowTask.IsStarted = 0 and DynaFlowTask.IsCompleted = 0 and DynaFlowTask.IsCanceled = 0 and DynaFlowTask.IsCancelRequested = 0)  )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

