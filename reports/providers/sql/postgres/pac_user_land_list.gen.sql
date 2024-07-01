DO $$

BEGIN

	SELECT * FROM
	(
		SELECT

			land.code as land_code,

			land.description as land_description,

			land.display_order as land_display_order,

			land.is_active as land_is_active,

			land.lookup_enum_name as land_lookup_enum_name,

			land.name as land_name,

			pac.name as pac_name,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'LandDescription' THEN land.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'LandDisplayOrder' THEN land.display_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'LandIsActive' THEN land.is_active  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'LandLookupEnumName' THEN land.lookup_enum_name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'LandName' THEN land.name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'PacName' THEN pac.name  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'LandDescription' THEN land.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'LandDisplayOrder' THEN land.display_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'LandIsActive' THEN land.is_active  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'LandLookupEnumName' THEN land.lookup_enum_name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'LandName' THEN land.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'PacName' THEN pac.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_land land on pac.pac_id = land.pac_id		 --child obj

		where
			 (pac.code = :context_code
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page);
END $$;
