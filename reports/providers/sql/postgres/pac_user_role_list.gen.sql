

	SELECT * FROM
	(
		SELECT

			role.code as role_code,

			role.description as role_description,

			role.display_order as role_display_order,

			role.is_active as role_is_active,

			role.lookup_enum_name as role_lookup_enum_name,

			role.name as role_name,

			pac.name as pac_name,

			ROW_NUMBER() OVER(
				ORDER BY

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'RoleDescription' THEN role.description  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'RoleDisplayOrder' THEN role.display_order  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'RoleIsActive' THEN role.is_active  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'RoleLookupEnumName' THEN role.lookup_enum_name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'RoleName' THEN role.name  END ASC,

					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'PacName' THEN pac.name  END ASC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'RoleDescription' THEN role.description  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'RoleDisplayOrder' THEN role.display_order  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'RoleIsActive' THEN role.is_active  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'RoleLookupEnumName' THEN role.lookup_enum_name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'RoleName' THEN role.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'PacName' THEN pac.name  END DESC,

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC

				) AS ROWNUMBER
		  -- select *
		from
		 	farm_pac  pac  --owner obj

			  join farm_role role on pac.pac_id = role.pac_id		 --child obj

		where
			 (pac.code = :context_code
			   )

	) AS TBL
	WHERE
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page)

