

		--TriStateFilter IsBuildTaskDebugRequiredTriStateFilterCode
		-- DECLARE @IsBuildTaskDebugRequiredTriStateFilterCode_TriStateFilterValue int = -1
		-- select @IsBuildTaskDebugRequiredTriStateFilterCode_TriStateFilterValue = StateIntValue from TriStateFilter where code = :is_build_task_debug_required_tri_state_filter_code

	SELECT * FROM
	(
		SELECT

			dyna_flowdyna_flow_type.name as dyna_flow_type_name,

			dyna_flow.description as description,

			dyna_flow.requested_utc_date_time as requested_utc_date_time,

			dyna_flow.is_build_task_debug_required as is_build_task_debug_required,

			dyna_flow.is_started as is_started,

			dyna_flow.started_utc_date_time as started_utc_date_time,

			dyna_flow.is_completed as is_completed,

			dyna_flow.completed_utc_date_time as completed_utc_date_time,

			dyna_flow.is_successful as is_successful,

			dyna_flow.code as dyna_flow_code,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'DynaFlowTypeName' THEN dyna_flowdyna_flow_type.name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'Description' THEN dyna_flow.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'RequestedUTCDateTime' THEN dyna_flow.requested_utc_date_time  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsBuildTaskDebugRequired' THEN dyna_flow.is_build_task_debug_required  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'StartedUTCDateTime' THEN dyna_flow.started_utc_date_time  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'CompletedUTCDateTime' THEN dyna_flow.completed_utc_date_time  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsSuccessful' THEN dyna_flow.is_successful  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'DynaFlowTypeName' THEN dyna_flowdyna_flow_type.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'Description' THEN dyna_flow.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'RequestedUTCDateTime' THEN dyna_flow.requested_utc_date_time  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsBuildTaskDebugRequired' THEN dyna_flow.is_build_task_debug_required  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'StartedUTCDateTime' THEN dyna_flow.started_utc_date_time  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'CompletedUTCDateTime' THEN dyna_flow.completed_utc_date_time  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsSuccessful' THEN dyna_flow.is_successful  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_dyna_flow dyna_flow on pac.pac_id = dyna_flow.pac_id		 --child obj

			left join farm_dyna_flow_type dyna_flowdyna_flow_type on dyna_flow.dyna_flow_type_id = dyna_flowdyna_flow_type.dyna_flow_type_id --child obj lookup prop

		where
			 (pac.code = :context_code
			   )

				--TriStateFilter IsBuildTaskDebugRequiredTriStateFilterCode @IsBuildTaskDebugRequiredTriStateFilterCode_TriStateFilterValue
			and (:is_build_task_debug_required_tri_state_filter_code is null or :is_build_task_debug_required_tri_state_filter_code = '00000000-0000-0000-0000-000000000000' or 
				(
					(
						select 
							state_int_value 
						from 
							farm_tri_state_filter 
						where code = :is_build_task_debug_required_tri_state_filter_code
					) in (
					-1,
					dyna_flow.is_build_task_debug_required
					)
				) 
			)

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

