# business/plant.py
# pylint: disable=unused-import
"""
"""
import uuid
from decimal import Decimal  # noqa: F401
from typing import List
from helpers.session_context import SessionContext
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
    async def get_land_plant_list(
        self,
        flavor_code: uuid.UUID = uuid.UUID(int=0),
        some_int_val: int = 0,
        some_big_int_val: int = 0,
        some_bit_val: bool = False,
        is_edit_allowed: bool = False,
        is_delete_allowed: bool = False,
        some_float_val: float = 0,
        some_decimal_val: Decimal = Decimal(0),
    ) -> List[ReportItemLandPlantList]:
        """
        Get the land plant list report.

        Args:
            land_code (str): The land code.
            flavor_code (str): The flavor code.
            some_int_val (int): The some int val.
            some_big_int_val (int): The some big int val.
            some_bit_val (bool): The some bit val.
            is_edit_allowed (bool): The is edit allowed.
            is_delete_allowed (bool): The is delete allowed.
            some_float_val (float): The some float val.
            some_decimal_val (float): The some decimal val.

        Returns:
            List[ReportItemLandPlantList]: The land plant list report.
        """
        report_manager = ReportManagerLandPlantList(self._session_context)
        return await report_manager.generate(
            self.land_code_peek,
            flavor_code,
            some_int_val,
            some_big_int_val,
            some_bit_val,
            is_edit_allowed,
            is_delete_allowed,
            some_float_val,
            some_decimal_val,
        )
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b]End
##GENLOOPReportEnd
##GENLearn[modelType=object,name=Land]End
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
