# business/plant.py
# pylint: disable=unused-import
"""
"""
import uuid
from decimal import Decimal  # noqa: F401
from datetime import date, datetime  # noqa: F401
from typing import List
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Plant
import models
import managers as managers_and_enums  # noqa: F401
##GENLOOPObjectStart
##GENTrainingBlock[a]Start
##GENLearn[modelType=object,name=Land]Start
##GENLOOPReportStart
##GENTrainingBlock[b]Start
##GENLearn[modelType=report,name=LandPlantList]Start
from reports import (  # noqa: F401
    ReportManagerLandPlantList,
    ReportItemLandPlantList)
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b]End
##GENLOOPReportEnd
##GENLearn[modelType=object,name=Land]End
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
from .plant_fluent import PlantFluentBusObj


class PlantReportsBusObj(PlantFluentBusObj):
    """
    """

##GENLOOPObjectStart
##GENTrainingBlock[a]Start
##GENLearn[modelType=object,name=Land]Start
##GENLOOPReportStart
##GENTrainingBlock[b]Start
##GENLearn[modelType=report,name=LandPlantList]Start
    async def generate_report_land_plant_list(
        self,
        flavor_code:
            uuid.UUID = uuid.UUID(int=0),
        some_int_val:
            int = 0,
        some_big_int_val:
            int = 0,
        some_bit_val:
            bool = False,
        is_edit_allowed:
            bool = False,
        is_delete_allowed:
            bool = False,
        some_float_val:
            float = 0,
        some_decimal_val:
            Decimal = Decimal(0),
        some_min_utc_date_time_val:
            datetime = TypeConversion.get_default_date_time(),
        some_min_date_val:
            date = TypeConversion.get_default_date(),
        some_money_val:
            Decimal = Decimal(0),
        some_n_var_char_val:
            str = "",
        some_var_char_val:
            str = "",
        some_text_val:
            str = "",
        some_phone_number:
            str = "",
        some_email_address:
            str = "",
# endset  # noqa: E122
        page_number: int = 1,
        item_count_per_page: int = 1,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[ReportItemLandPlantList]:
        """
        Get the land plant list report.

        Returns:
            List[ReportItemLandPlantList]: The land plant list report.
        """
        report_manager = ReportManagerLandPlantList(self._session_context)
        return await report_manager.generate(
            self.land_code_peek,
# endset  # noqa: E122
            flavor_code,
            some_int_val,
            some_big_int_val,
            some_bit_val,
            is_edit_allowed,
            is_delete_allowed,
            some_float_val,
            some_decimal_val,
            some_min_utc_date_time_val,
            some_min_date_val,
            some_money_val,
            some_n_var_char_val,
            some_var_char_val,
            some_text_val,
            some_phone_number,
            some_email_address,
# endset  # noqa: E122
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b]End
##GENLOOPReportEnd
##GENLearn[modelType=object,name=Land]End
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
