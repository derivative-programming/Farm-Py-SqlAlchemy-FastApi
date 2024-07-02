
    async def generate_report_GENVALSnakeReportName(
        self,
//GENLOOPReportParamStart
//GENIGNOREDATATYPE

//GENIF[calculatedSqlServerDBDataType=uniqueidentifier]Start
        GENVALSnakeReportParamName:
            uuid.UUID = uuid.UUID(int=0),
//GENIF[calculatedSqlServerDBDataType=uniqueidentifier]End
//GENIF[calculatedSqlServerDBDataType=int]Start
        GENVALSnakeReportParamName:
            int = 0,
//GENIF[calculatedSqlServerDBDataType=int]End
//GENIF[calculatedSqlServerDBDataType=bigint]Start
        GENVALSnakeReportParamName:
            int = 0,
//GENIF[calculatedSqlServerDBDataType=bigint]End
//GENIF[calculatedSqlServerDBDataType=bit]Start
        GENVALSnakeReportParamName:
            bool = False,
//GENIF[calculatedSqlServerDBDataType=bit]End
//GENIF[calculatedSqlServerDBDataType=float]Start
        GENVALSnakeReportParamName:
            float = 0,
//GENIF[calculatedSqlServerDBDataType=float]End
//GENIF[calculatedSqlServerDBDataType=decimal]Start
        GENVALSnakeReportParamName:
            Decimal = Decimal(0),
//GENIF[calculatedSqlServerDBDataType=decimal]End
//GENIF[calculatedSqlServerDBDataType=datetime]Start
        GENVALSnakeReportParamName:
            datetime = TypeConversion.get_default_date_time(),
//GENIF[calculatedSqlServerDBDataType=datetime]End
//GENIF[calculatedSqlServerDBDataType=date]Start
        GENVALSnakeReportParamName:
            date = TypeConversion.get_default_date(),
//GENIF[calculatedSqlServerDBDataType=date]End
//GENIF[calculatedSqlServerDBDataType=money]Start
        GENVALSnakeReportParamName:
            Decimal = Decimal(0),
//GENIF[calculatedSqlServerDBDataType=money]End
//GENIF[calculatedSqlServerDBDataType=nvarchar]Start
        GENVALSnakeReportParamName:
            str = "",
//GENIF[calculatedSqlServerDBDataType=nvarchar]End
//GENIF[calculatedSqlServerDBDataType=varchar]Start
        GENVALSnakeReportParamName:
            str = "",
//GENIF[calculatedSqlServerDBDataType=varchar]End
//GENIF[calculatedSqlServerDBDataType=text]Start
        GENVALSnakeReportParamName:
            str = "",
//GENIF[calculatedSqlServerDBDataType=text]End


//GENLOOPReportParamEnd
        page_number: int = 1,
        item_count_per_page: int = 100,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[reports_managers.ReportItemGENVALPascalReportName]:
        """
        Get the GENVALSpacedReportName report.

        Returns:
            List[ReportItemGENVALPascalReportName]: The GENVALSpacedReportName report.
        """
        report_manager = reports_managers. \
            ReportManagerGENVALPascalReportName(
                self._session_context)
        return await report_manager.generate(
            self.code,
//GENLOOPReportParamStart
//GENIGNOREDATATYPE

//GENIF[calculatedSqlServerDBDataType=uniqueidentifier]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=uniqueidentifier]End
//GENIF[calculatedSqlServerDBDataType=int]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=int]End
//GENIF[calculatedSqlServerDBDataType=bigint]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=bigint]End
//GENIF[calculatedSqlServerDBDataType=bit]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=bit]End
//GENIF[calculatedSqlServerDBDataType=float]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=float]End
//GENIF[calculatedSqlServerDBDataType=decimal]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=decimal]End
//GENIF[calculatedSqlServerDBDataType=datetime]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=datetime]End
//GENIF[calculatedSqlServerDBDataType=date]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=date]End
//GENIF[calculatedSqlServerDBDataType=money]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=money]End
//GENIF[calculatedSqlServerDBDataType=nvarchar]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=nvarchar]End
//GENIF[calculatedSqlServerDBDataType=varchar]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=varchar]End
//GENIF[calculatedSqlServerDBDataType=text]Start
            GENVALSnakeReportParamName,
//GENIF[calculatedSqlServerDBDataType=text]End


//GENLOOPReportParamEnd
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
