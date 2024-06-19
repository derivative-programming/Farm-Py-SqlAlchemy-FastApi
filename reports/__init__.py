# __init__.py

"""
This module contains the reports package.

The reports package provides functionality for
generating various reports
"""

from .report_request_validation_error import (  # noqa: F401
    ReportRequestValidationError)
##GENLOOPObjectStart
##GENTrainingBlock[a]Start
##GENLearn[modelType=object,name=Land]Start
##GENLOOPReportStart
##GENTrainingBlock[b]Start
##GENLearn[modelType=report,name=LandPlantList]Start
from .land_plant_list import (  # noqa: F401
    ReportManagerLandPlantList)
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b]End
##GENLOOPReportEnd
##GENLearn[modelType=object,name=Land]End
from .tac_farm_dashboard import (  # noqa: F401
    ReportManagerTacFarmDashboard)
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
