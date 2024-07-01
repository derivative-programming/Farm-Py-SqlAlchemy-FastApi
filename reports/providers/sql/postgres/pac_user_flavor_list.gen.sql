DO $$

BEGIN

	SELECT * FROM
	(
		SELECT

			flavor.code as flavor_code,

			flavor.description as flavor_description,

			flavor.display_order as flavor_display_order,

			flavor.is_active as flavor_is_active,

			flavor.lookup_enum_name as flavor_lookup_enum_name,

			flavor.name as flavor_name,

			pac.name as pac_name,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'FlavorDescription' THEN flavor.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'FlavorDisplayOrder' THEN flavor.display_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'FlavorIsActive' THEN flavor.is_active  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'FlavorLookupEnumName' THEN flavor.lookup_enum_name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'FlavorName' THEN flavor.name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'PacName' THEN pac.name  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'FlavorDescription' THEN flavor.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'FlavorDisplayOrder' THEN flavor.display_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'FlavorIsActive' THEN flavor.is_active  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'FlavorLookupEnumName' THEN flavor.lookup_enum_name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'FlavorName' THEN flavor.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'PacName' THEN pac.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_flavor flavor on pac.pac_id = flavor.pac_id		 --child obj

		where
			 (pac.code = :context_code
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page);
END $$;
