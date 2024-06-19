# apis/models/init/__init__.py

"""
This module contains the initialization code for the models used in the APIs.

The models include:
- Land
- LandAddPlantInitObjWF
- LandPlantListInitReport
- TacFarmDashboardInitReport
- TacLoginInitObjWF
- TacRegisterInitObjWF
- CustomerUserLogOutInitObjWF
- PacUserDateGreaterThanFilterListInitReport
- PacUserFlavorListInitReport
- PacUserLandListInitReport
- PacUserRoleListInitReport
- PacUserTacListInitReport
- PacUserTriStateFilterListInitReport
- PlantUserDetailsInitReport
"""

##GENLOOPObjectStart
##GENTrainingBlock[a]Start
##GENLearn[modelType=object,name=Land]Start
##GENLOOPObjectWorkflowStart
##GENTrainingBlock[b]Start
##GENLearn[modelType=objectWorkflow,name=LandAddPlantInitObjWF,calculatedIsInitObjWF=true]Start
from .land_add_plant_init_obj_wf import (  # noqa: F401
    LandAddPlantInitObjWFGetInitModelRequest,
    LandAddPlantInitObjWFGetInitModelResponse)
##GENLearn[modelType=objectWorkflow,name=LandAddPlantInitObjWF,calculatedIsInitObjWF=true]End
##GENTrainingBlock[b]End
##GENLOOPObjectWorkflowEnd
##GENLearn[modelType=object,name=Land]End
from .land_plant_list_init_report import (  # noqa: F401
    LandPlantListInitReportGetInitModelRequest,
    LandPlantListInitReportGetInitModelResponse)
from .tac_farm_dashboard_init_report import (  # noqa: F401
    TacFarmDashboardInitReportGetInitModelRequest,
    TacFarmDashboardInitReportGetInitModelResponse)
from .tac_login_init_obj_wf import (  # noqa: F401
    TacLoginInitObjWFGetInitModelRequest,
    TacLoginInitObjWFGetInitModelResponse)
from .tac_register_init_obj_wf import (  # noqa: F401
    TacRegisterInitObjWFGetInitModelRequest,
    TacRegisterInitObjWFGetInitModelResponse)
from .customer_user_log_out_init_obj_wf import (  # noqa: F401
    CustomerUserLogOutInitObjWFGetInitModelRequest,
    CustomerUserLogOutInitObjWFGetInitModelResponse)
from .pac_user_date_greater_than_filter_list_init_report import (  # noqa: F401
    PacUserDateGreaterThanFilterListInitReportGetInitModelRequest,
    PacUserDateGreaterThanFilterListInitReportGetInitModelResponse)
from .pac_user_flavor_list_init_report import (  # noqa: F401
    PacUserFlavorListInitReportGetInitModelRequest,
    PacUserFlavorListInitReportGetInitModelResponse)
from .pac_user_land_list_init_report import (  # noqa: F401
    PacUserLandListInitReportGetInitModelRequest,
    PacUserLandListInitReportGetInitModelResponse)
from .pac_user_role_list_init_report import (  # noqa: F401
    PacUserRoleListInitReportGetInitModelRequest,
    PacUserRoleListInitReportGetInitModelResponse)
from .pac_user_tac_list_init_report import (  # noqa: F401
    PacUserTacListInitReportGetInitModelRequest,
    PacUserTacListInitReportGetInitModelResponse)
from .pac_user_tri_state_filter_list_init_report import (  # noqa: F401
    PacUserTriStateFilterListInitReportGetInitModelRequest,
    PacUserTriStateFilterListInitReportGetInitModelResponse)
from .plant_user_details_init_report import (  # noqa: F401
    PlantUserDetailsInitReportGetInitModelRequest,
    PlantUserDetailsInitReportGetInitModelResponse)
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
