

	SELECT * FROM
	(
		SELECT

			dyna_flow.code as dyna_flow_code,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_dyna_flow dyna_flow on pac.pac_id = dyna_flow.pac_id		 --child obj

			left join farm_dyna_flow_type dyna_flowdyna_flow_type on dyna_flow.dyna_flow_type_id = dyna_flowdyna_flow_type.dyna_flow_type_id --child obj lookup prop

		where
			 (pac.code = :context_code
			 And DynaFlow.IsStarted = 1 and DynaFlow.IsSuccessful = 0 and DynaFlow.IsCanceled = 0 and DynaFlow.IsCancelRequested = 0 and DynaFlow.IsTasksCreated = 0 and DynaFlow.IsTaskCreationStarted = 1 and DynaFlow.StartedUTCDateTime < dateadd(HOUR,-2,getutcdate())  )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

