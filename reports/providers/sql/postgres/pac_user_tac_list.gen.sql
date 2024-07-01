DO $$

BEGIN

	SELECT * FROM
	(
		SELECT

			tac.code as tac_code,

			tac.description as tac_description,

			tac.display_order as tac_display_order,

			tac.is_active as tac_is_active,

			tac.lookup_enum_name as tac_lookup_enum_name,

			tac.name as tac_name,

			pac.name as pac_name,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TacDescription' THEN tac.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TacDisplayOrder' THEN tac.display_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TacIsActive' THEN tac.is_active  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TacLookupEnumName' THEN tac.lookup_enum_name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'TacName' THEN tac.name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'PacName' THEN pac.name  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TacDescription' THEN tac.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TacDisplayOrder' THEN tac.display_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TacIsActive' THEN tac.is_active  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TacLookupEnumName' THEN tac.lookup_enum_name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'TacName' THEN tac.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'PacName' THEN pac.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_tac tac on pac.pac_id = tac.pac_id		 --child obj

		where
			 (pac.code = :context_code
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page);
END $$;
