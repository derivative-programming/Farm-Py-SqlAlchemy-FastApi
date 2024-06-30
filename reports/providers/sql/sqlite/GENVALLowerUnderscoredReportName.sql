
               
        --GENLOOPReportParamStart
		--GENIF[calculatedFKObjectName=TriStateFilter]Start
		--TriStateFilter GENVALName
		-- DECLARE @GENVALName_TriStateFilterValue int = -1
		-- select @GENVALName_TriStateFilterValue = state_int_value from farm_tri_state_filter where code = :GENVALLowerUnderscoredReportParamName
		--GENIF[calculatedFKObjectName=TriStateFilter]End
		--GENIF[calculatedFKObjectName=DateGreaterThanFilter]Start
		--DateGreaterThanFilter GENVALName
		DECLARE @GENVALName_DateGreaterThanFilterIntValue int = -1
		select @GENVALName_DateGreaterThanFilterIntValue = DayCount from farm_date_greater_than_filter where code = :GENVALLowerUnderscoredReportParamName
		DECLARE @GENVALName_DateGreaterThanFilterUtcDateTimeValue datetime = getutcdate()
		select @GENVALName_DateGreaterThanFilterUtcDateTimeValue = dateadd(d,(-1 * @GENVALName_DateGreaterThanFilterIntValue),getutcdate())
		--GENIF[calculatedFKObjectName=DateGreaterThanFilter]End
        --GENLOOPReportParamEnd

   
	SELECT * FROM 
	(
		SELECT    
        --GENLOOPReportColumnStart
		--GENIF[calculatedIsSourceObjectAvailable=true]Start
			GENVALLowerUnderscoredcalculatedSourceLookupObjImplementationObjNameGENVALLowerUnderscoredcalculatedSourceObjectName.GENVALLowerUnderscoredcalculatedSourcePropertyName as GENVALLowerUnderscoredReportColumnName,
		--GENIF[calculatedIsSourceObjectAvailable=true]End
		--GENIF[calculatedIsSourceObjectAvailable=false]Start
				--GENCASE[calculatedCSharpDataType]Start
				--GENWHEN[Guid]Start 
			GENVALLowerUnderscoredObjectName.code as GENVALLowerUnderscoredReportColumnName,
				--GENWHEN[Guid]End
				--GENWHEN[Boolean]Start 
				--GENIF[calculatedIsConditionalSqlLogicAvailable=false]Start 
			GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredReportColumnName as GENVALLowerUnderscoredReportColumnName,
				--GENIF[calculatedIsConditionalSqlLogicAvailable=false]End
				--GENIF[calculatedIsConditionalSqlLogicAvailable=true]Start 
			cast((case when GENVALconditionalSqlLogic then 1 else 0 end) as bit) as GENVALLowerUnderscoredReportColumnName,
				--GENIF[calculatedIsConditionalSqlLogicAvailable=true]End
				--GENWHEN[Boolean]End
				--GENElseStart  
			GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredReportColumnName as GENVALLowerUnderscoredReportColumnName,
				--GENElseEnd 
				--GENCASE[calculatedCSharpDataType]End 
		--GENIF[calculatedIsSourceObjectAvailable=false]End
		--GENLOOPReportColumnEnd  
			ROW_NUMBER() OVER(
				ORDER BY 

				
		--GENIF[calculatedIsVisualizationDetailThreeColumn=false]Start 
		--GENIF[calculatedIsVisualizationDetailTwoColumn=false]Start 
				
        --GENLOOPReportColumnStart  
				--GENFILTER[isVisible=true]  
				--GENIF[calculatedIsSourceObjectAvailable=true]Start
				--GENCASE[calculatedSqlServerDBDataType]Start
				--GENWHEN[Uniqueidentifier]Start 
				--GENWHEN[Uniqueidentifier]End
				--GENWHEN[Text]Start 
				--GENWHEN[Text]End
				--GENElseStart  
					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'GENVALReportColumnName' THEN GENVALLowerUnderscoredcalculatedSourceLookupObjImplementationObjNameGENVALLowerUnderscoredcalculatedSourceObjectName.GENVALLowerUnderscoredcalculatedSourcePropertyName  END ASC, 
				--GENElseEnd 
				--GENCASE[calculatedSqlServerDBDataType]End 
				--GENIF[calculatedIsSourceObjectAvailable=true]End
				--GENIF[calculatedIsSourceObjectAvailable=false]Start
				--GENCASE[calculatedSqlServerDBDataType]Start
				--GENWHEN[Uniqueidentifier]Start 
				--GENWHEN[Uniqueidentifier]End
				--GENWHEN[Text]Start 
				--GENWHEN[Text]End
				--GENElseStart  
					CASE WHEN :order_by_descending = 0 and :order_by_column_name = 'GENVALReportColumnName' THEN GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredReportColumnName  END ASC, 
				--GENElseEnd 
				--GENCASE[calculatedSqlServerDBDataType]End 
				--GENIF[calculatedIsSourceObjectAvailable=false]End 
        --GENLOOPReportColumnEnd   


        --GENLOOPReportColumnStart 
				--GENFILTER[isVisible=true]  
				--GENIF[calculatedIsSourceObjectAvailable=true]Start
				--GENCASE[calculatedSqlServerDBDataType]Start
				--GENWHEN[Uniqueidentifier]Start 
				--GENWHEN[Uniqueidentifier]End
				--GENWHEN[Text]Start 
				--GENWHEN[Text]End
				--GENElseStart  
					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'GENVALReportColumnName' THEN GENVALLowerUnderscoredcalculatedSourceLookupObjImplementationObjNameGENVALLowerUnderscoredcalculatedSourceObjectName.GENVALLowerUnderscoredcalculatedSourcePropertyName  END DESC, 
				--GENElseEnd 
				--GENCASE[calculatedSqlServerDBDataType]End
				--GENIF[calculatedIsSourceObjectAvailable=true]End
				--GENIF[calculatedIsSourceObjectAvailable=false]Start
				--GENCASE[calculatedSqlServerDBDataType]Start
				--GENWHEN[Uniqueidentifier]Start 
				--GENWHEN[Uniqueidentifier]End
				--GENWHEN[Text]Start 
				--GENWHEN[Text]End
				--GENElseStart  
					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'GENVALReportColumnName' THEN GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredReportColumnName  END DESC, 
				--GENElseEnd 
				--GENCASE[calculatedSqlServerDBDataType]End
				--GENIF[calculatedIsSourceObjectAvailable=false]End 
        --GENLOOPReportColumnEnd
		
		--GENIF[calculatedIsVisualizationDetailTwoColumn=false]End 
		--GENIF[calculatedIsVisualizationDetailThreeColumn=false]End 

					CASE WHEN :order_by_descending = 1 and :order_by_column_name = 'placeholder' THEN ''  END DESC 

				) AS ROWNUMBER 
		  -- select * 
		from 
		 	farm_GENVALLowerUnderscoredObjectName  GENVALLowerUnderscoredObjectName  --owner obj
			
			--GENIF[calculatedIsTargetChildObjectAvailable=true]Start
			--GENIF[calculatedIsTrueParentChild=false]Start
			--left join farm_GENVALLowerUnderscoredcalculatedTargetChildObject GENVALLowerUnderscoredcalculatedTargetChildObject on 1=1			
			--GENIF[calculatedIsTrueParentChild=false]End
			--GENIF[calculatedIsTrueParentChild=true]Start
			  join farm_GENVALLowerUnderscoredcalculatedTargetChildObject GENVALLowerUnderscoredcalculatedTargetChildObject on GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredObjectName_id = GENVALLowerUnderscoredcalculatedTargetChildObject.GENVALLowerUnderscoredObjectName_id		 --child obj
			--GENLOOPchildObjLookupsSTART
			left join farm_GENVALLowerUnderscoredlookupName GENVALLowerUnderscoredcalculatedTargetChildObjectGENVALLowerUnderscoredlookupName on GENVALLowerUnderscoredcalculatedTargetChildObject.GENVALLowerUnderscoredimplementationPropName = GENVALLowerUnderscoredcalculatedTargetChildObjectGENVALLowerUnderscoredlookupName.GENVALLowerUnderscoredlookupName_id --child obj lookup prop
			--GENLOOPchildObjLookupsEnd 
			--GENIF[calculatedIsTrueParentChild=true]End 
			--GENIF[calculatedIsTargetChildObjectAvailable=true]End
			
			--GENLOOPPropSTART
			--GENIF[isFK=true]Start
			--GENIF[calculatedisFKObjectParentOFOwnerObject=false]Start
			--GENIF[isFKLookup=false]Start
			left join farm_GENVALLowerUnderscoredPROPcalculatedFKObjectName GENVALLowerUnderscoredPROPcalculatedFKObjectName on GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredPropName = GENVALLowerUnderscoredPROPcalculatedFKObjectName.GENVALLowerUnderscoredPROPcalculatedFKObjectPropertyName   -- fk prop
			--GENIF[isFKLookup=false]End
			--GENIF[isFKLookup=true]Start
			left join farm_GENVALLowerUnderscoredPROPcalculatedFKObjectName GENVALLowerUnderscoredObjectNameGENVALPROPcalculatedFKObjectName on GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredPropName = GENVALLowerUnderscoredObjectNameGENVALPROPcalculatedFKObjectName.GENVALLowerUnderscoredPROPcalculatedFKObjectPropertyName   -- fk prop
			--GENIF[isFKLookup=true]End
			--GENIF[calculatedisFKObjectParentOFOwnerObject=false]End  
			--GENIF[isFK=true]End 
			--GENLOOPPropEnd  
			
			--GENLOOPobjTreePathSTART   
			left join farm_GENVALLowerUnderscoredparentObjName GENVALLowerUnderscoredparentObjName on GENVALLowerUnderscoredparentObjName.GENVALLowerUnderscoredparentObjName_id = GENVALLowerUnderscoredchildObjName.GENVALLowerUnderscoredchildPropName  -- up obj tree
			--GENLOOPparentObjLookupsSTART   
			left join farm_GENVALLowerUnderscoredlookupName GENVALLowerUnderscoredparentObjNameGENVALlookupName on GENVALLowerUnderscoredparentObjName.GENVALLowerUnderscoredimplementationPropName = GENVALLowerUnderscoredparentObjNameGENVALlookupName.GENVALLowerUnderscoredlookupName_id -- tree parent obj lookup prop
			--GENLOOPparentObjLookupsEnd 
			--GENLOOPobjTreePathEnd 
			 

			--GENLOOPobjJoinTreeSTART   
			left join farm_GENVALLowerUnderscoredchildObjName GENVALLowerUnderscoredchildObjName on GENVALLowerUnderscoredchildObjName.GENVALLowerUnderscoredchildPropName = GENVALLowerUnderscoredparentObjName.GENVALLowerUnderscoredparentObjName_id  -- up obj join tree
			--GENLOOPchildObjLookupsSTART   
			left join farm_GENVALLowerUnderscoredlookupName GENVALLowerUnderscoredchildObjNameGENVALLowerUnderscoredlookupName on GENVALLowerUnderscoredchildObjName.GENVALLowerUnderscoredimplementationPropName = GENVALLowerUnderscoredchildObjNameGENVALlookupName.GENVALLowerUnderscoredlookupName_id -- join tree hild obj lookup prop
			--GENLOOPchildObjLookupsEnd 
			--GENLOOPobjJoinTreeEnd 
			
			--GENIF[calculatedIsTargetChildObjAPairedIntersectionObj=true]Start
			--GENLOOPintersectionObjSTART 
			--owner obj intersection table  
			join  farm_GENVALLowerUnderscoredName GENVALLowerUnderscoredName on GENVALLowerUnderscoredName.GENVALLowerUnderscoredObjectName_id = GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredObjectName_id
			join farm_GENVALLowerUnderscoredpairedObj GENVALLowerUnderscoredpairedObj on GENVALLowerUnderscoredName.GENVALLowerUnderscoredpairedObj_id = GENVALLowerUnderscoredpairedObj.GENVALLowerUnderscoredpairedObj_id
			--GENLOOPintersectionObjEnd
			--GENIF[calculatedIsTargetChildObjAPairedIntersectionObj=true]End
			
			
			--GENIF[calculatedIsTargetChildObjAPairedIntersectionObj=false]Start
			--GENLOOPintersectionObjSTART 
			--owner obj intersection table , 1st record only
			left join farm_GENVALLowerUnderscoredName GENVALLowerUnderscoredName on GENVALLowerUnderscoredName.GENVALLowerUnderscoredObjectName_id = GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredObjectName_id
			left join farm_GENVALLowerUnderscoredName GENVALLowerUnderscoredName2 on GENVALLowerUnderscoredName.GENVALLowerUnderscoredObjectName_id = GENVALLowerUnderscoredName2.GENVALLowerUnderscoredObjectName_id and GENVALLowerUnderscoredName.GENVALLowerUnderscoredName_id > GENVALLowerUnderscoredName2.GENVALLowerUnderscoredName_id
			--GENLOOPintersectionObjEnd
			--GENIF[calculatedIsTargetChildObjAPairedIntersectionObj=false]End
			
			
			--GENLOOPtargetChildObjectIntersectionObjSTART 
			--target child obj intersection table , 1st record only
			left join farm_GENVALLowerUnderscoredName GENVALLowerUnderscoredName on GENVALLowerUnderscoredName.GENVALLowerUnderscoredcalculatedTargetChildObjectID = GENVALLowerUnderscoredcalculatedTargetChildObject.GENVALLowerUnderscoredcalculatedTargetChildObjectID
			left join farm_GENVALLowerUnderscoredName GENVALLowerUnderscoredName2 on GENVALLowerUnderscoredName.GENVALLowerUnderscoredcalculatedTargetChildObjectID = GENVALLowerUnderscoredName2.GENVALLowerUnderscoredcalculatedTargetChildObjectID and GENVALLowerUnderscoredName.GENVALLowerUnderscoredName_id > GENVALLowerUnderscoredName2.GENVALLowerUnderscoredName_id
			--left join farm_GENVALpairedObj GENVALpairedObj on GENVALLowerUnderscoredName.GENVALLowerUnderscoredpairedObj_id = GENVALpairedObj.GENVALpairedObjID
			--GENLOOPtargetChildObjectIntersectionObjEnd
			
			--GENIF[calculatedIsRowLevelOrgCustomerSecurityUsed=true]Start 
			join farm_customer Customer_Security on farm_org_customer.CustomerID = Customer_Security.CustomerID
			--GENIF[calculatedIsRowLevelOrgCustomerSecurityUsed=true]End
			
			--GENIF[calculatedIsRowLevelOrganizationSecurityUsed=true]Start
			join farm_org_customer orgCustomer_Security on orgCustomer_Security.OrganizationID = farm_organization.OrganizationID
			join farm_customer Customer_Security on farm_org_customer_Security.CustomerID = Customer_Security.CustomerID
			--GENIF[calculatedIsRowLevelOrganizationSecurityUsed=true]End

		where
			 (GENVALLowerUnderscoredObjectName.code = :context_code
			 GENVALfilteringSqlLogic  )
			--GENIF[calculatedIsRowLevelCustomerSecurityUsed=true]Start
			and (:user_id is not null and :user_id <> '00000000-0000-0000-0000-000000000000' and Customer.Code = :user_id )
			--GENIF[calculatedIsRowLevelCustomerSecurityUsed=true]End

			--GENIF[calculatedIsRowLevelOrgCustomerSecurityUsed=true]Start
			and (:user_id is not null and :user_id <> '00000000-0000-0000-0000-000000000000' and Customer_Security.Code = :user_id )
			--GENIF[calculatedIsRowLevelOrgCustomerSecurityUsed=true]End

			--GENIF[calculatedIsRowLevelOrganizationSecurityUsed=true]Start
			and (:user_id is not null and :user_id <> '00000000-0000-0000-0000-000000000000' and Customer_Security.Code = :user_id )
			--GENIF[calculatedIsRowLevelOrganizationSecurityUsed=true]End
			 
			--GENIF[calculatedIsTargetChildObjAPairedIntersectionObj=false]Start
			--GENLOOPintersectionObjSTART  
			and GENVALLowerUnderscoredName2.GENVALLowerUnderscoredName_id is null
			--GENLOOPintersectionObjEnd
			--GENIF[calculatedIsTargetChildObjAPairedIntersectionObj=false]End
			
			--GENLOOPtargetChildObjectIntersectionObjSTART 
			and GENVALLowerUnderscoredName2.GENVALLowerUnderscoredName_id is null
			--GENLOOPtargetChildObjectIntersectionObjEnd

        --GENLOOPReportParamStart 
		--GENIF[calculatedIsTargetObjectAvailable=true]Start
			 	--GENCASE[calculatedCSharpDataType]Start
				--GENWHEN[String]Start 
			and (:GENVALLowerUnderscoredReportParamName is null or :GENVALLowerUnderscoredReportParamName = GENVALcalculatedSqlServerSingleQuoteDefaultValue or  GENVALLowerUnderscoredcalculatedTargetLookupObjImplementationObjNameGENVALLowerUnderscoredcalculatedTargetObjectName.GENVALLowerUnderscoredcalculatedTargetPropertyName like :like_GENVALLowerUnderscoredReportParamName)
				--GENWHEN[String]End
				--GENElseStart  
				
				--GENIF[calculatedFKObjectName=TriStateFilter]Start
				--TriStateFilter GENVALName @GENVALName_TriStateFilterValue
			and (
				:GENVALLowerUnderscoredReportParamName is null or 
				:GENVALLowerUnderscoredReportParamName = '00000000-0000-0000-0000-000000000000' or 
				(
					(
						select 
							state_int_value 
						from 
							farm_tri_state_filter 
						where code = :GENVALLowerUnderscoredReportParamName
					) in (
					-1,
					GENVALLowerUnderscoredcalculatedTargetLookupObjImplementationObjNameGENVALLowerUnderscoredcalculatedTargetObjectName.GENVALLowerUnderscoredcalculatedTargetPropertyName
					)
				)
				--GENIF[calculatedFKObjectName=TriStateFilter]End
				--GENIF[calculatedFKObjectName=DateGreaterThanFilter]Start
				--DateGreaterThanFilter GENVALName @GENVALName_DateGreaterThanFilterUtcDateTimeValue
			and (:GENVALLowerUnderscoredReportParamName is null or :GENVALLowerUnderscoredReportParamName = '00000000-0000-0000-0000-000000000000' or @GENVALName_DateGreaterThanFilterUtcDateTimeValue < GENVALLowerUnderscoredcalculatedTargetLookupObjImplementationObjNameGENVALLowerUnderscoredcalculatedTargetObjectName.GENVALLowerUnderscoredcalculatedTargetPropertyName)
				--GENIF[calculatedFKObjectName=DateGreaterThanFilter]End
				
				--GENIF[calculatedFKObjectName!=TriStateFilter]Start
				--GENIF[calculatedFKObjectName!=DateGreaterThanFilter]Start
			and (:GENVALLowerUnderscoredReportParamName is null or :GENVALLowerUnderscoredReportParamName = GENVALcalculatedSqlServerSingleQuoteDefaultValue or :GENVALLowerUnderscoredReportParamName = GENVALLowerUnderscoredcalculatedTargetLookupObjImplementationObjNameGENVALLowerUnderscoredcalculatedTargetObjectName.GENVALLowerUnderscoredcalculatedTargetPropertyName)
				--GENIF[calculatedFKObjectName!=DateGreaterThanFilter]End
				--GENIF[calculatedFKObjectName!=TriStateFilter]End

				--GENElseEnd 
				--GENCASE[calculatedCSharpDataType]End
		--GENIF[calculatedIsTargetObjectAvailable=true]End
		--GENIF[calculatedIsTargetObjectAvailable=false]Start
			 	--GENCASE[calculatedCSharpDataType]Start
				--GENWHEN[String]Start 
			and (:GENVALLowerUnderscoredReportParamName is null or :GENVALLowerUnderscoredReportParamName = GENVALcalculatedSqlServerSingleQuoteDefaultValue or  GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredReportParamName like :like_GENVALLowerUnderscoredReportParamName)
				--GENWHEN[String]End
				--GENElseStart  
			and (:GENVALLowerUnderscoredReportParamName is null or :GENVALLowerUnderscoredReportParamName = GENVALcalculatedSqlServerSingleQuoteDefaultValue or :GENVALLowerUnderscoredReportParamName = GENVALLowerUnderscoredObjectName.GENVALLowerUnderscoredReportParamName)
				--GENElseEnd 
				--GENCASE[calculatedCSharpDataType]End
		--GENIF[calculatedIsTargetObjectAvailable=false]End
        --GENLOOPReportParamEnd    
   
	) AS TBL
	WHERE 
		ROWNUMBER BETWEEN ((:page_number - 1) * :item_count_per_page + 1) AND (:page_number * :item_count_per_page) 
		  