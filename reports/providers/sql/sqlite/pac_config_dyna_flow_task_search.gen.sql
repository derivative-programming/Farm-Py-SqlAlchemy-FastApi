


	SELECT * FROM
	(
		SELECT

			dyna_flow_task.started_utc_date_time as started_utc_date_time,

			dyna_flow_task.processor_identifier as processor_identifier,

			dyna_flow_task.is_started as is_started,

			dyna_flow_task.is_completed as is_completed,

			dyna_flow_task.is_successful as is_successful,

			dyna_flow_task.code as dyna_flow_task_code,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'StartedUTCDateTime' THEN dyna_flow_task.started_utc_date_time  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'ProcessorIdentifier' THEN dyna_flow_task.processor_identifier  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsStarted' THEN dyna_flow_task.is_started  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsCompleted' THEN dyna_flow_task.is_completed  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'IsSuccessful' THEN dyna_flow_task.is_successful  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'StartedUTCDateTime' THEN dyna_flow_task.started_utc_date_time  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'ProcessorIdentifier' THEN dyna_flow_task.processor_identifier  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsStarted' THEN dyna_flow_task.is_started  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsCompleted' THEN dyna_flow_task.is_completed  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'IsSuccessful' THEN dyna_flow_task.is_successful  END DESC,

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

		where
			 (pac.code = :context_code
			   )
 
			and (:processor_identifier is null or :processor_identifier = '' or  dyna_flow_task.processor_identifier like :like_processor_identifier)

				--TriStateFilter IsStartedTriStateFilterCode @IsStartedTriStateFilterCode_TriStateFilterValue
			and (
				:is_started_tri_state_filter_code is null or
				:is_started_tri_state_filter_code = '00000000-0000-0000-0000-000000000000' or
				(
					(
						select
							state_int_value
						from
							farm_tri_state_filter
						where code = :is_started_tri_state_filter_code
					) in (
					-1,
					dyna_flow_task.is_started
					)
				)
			)

				--TriStateFilter IsCompletedTriStateFilterCode @IsCompletedTriStateFilterCode_TriStateFilterValue
			and (
				:is_completed_tri_state_filter_code is null or
				:is_completed_tri_state_filter_code = '00000000-0000-0000-0000-000000000000' or
				(
					(
						select
							state_int_value
						from
							farm_tri_state_filter
						where code = :is_completed_tri_state_filter_code
					) in (
					-1,
					dyna_flow_task.is_completed
					)
				)
			)

				--TriStateFilter IsSuccessfulTriStateFilterCode @IsSuccessfulTriStateFilterCode_TriStateFilterValue
			and (
				:is_successful_tri_state_filter_code is null or
				:is_successful_tri_state_filter_code = '00000000-0000-0000-0000-000000000000' or
				(
					(
						select
							state_int_value
						from
							farm_tri_state_filter
						where code = :is_successful_tri_state_filter_code
					) in (
					-1,
					dyna_flow_task.is_successful
					)
				)
			)

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

