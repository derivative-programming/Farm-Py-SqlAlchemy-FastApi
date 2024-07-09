# reports/__init__.py  # pylint: disable=duplicate-code # noqa: E501

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
from .row_models.land_plant_list import (  # noqa: F401
    ReportItemLandPlantList
)
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b]End
##GENLOOPReportEnd
##GENLearn[modelType=object,name=Land]End
from .tac_farm_dashboard import (  # noqa: F401
    ReportManagerTacFarmDashboard)
from .pac_user_date_greater_than_filter_list import (  # noqa: F401
    ReportManagerPacUserDateGreaterThanFilterList)
from .pac_user_flavor_list import (  # noqa: F401
    ReportManagerPacUserFlavorList)
from .pac_user_land_list import (  # noqa: F401
    ReportManagerPacUserLandList)
from .pac_user_role_list import (  # noqa: F401
    ReportManagerPacUserRoleList)
from .pac_user_tac_list import (  # noqa: F401
    ReportManagerPacUserTacList)
from .pac_user_tri_state_filter_list import (  # noqa: F401
    ReportManagerPacUserTriStateFilterList)
from .plant_user_details import (  # noqa: F401
    ReportManagerPlantUserDetails)

from .pac_user_dyna_flow_task_type_list import (  # noqa: F401
    ReportManagerPacUserDynaFlowTaskTypeList)
from .pac_user_dyna_flow_type_list import (  # noqa: F401
    ReportManagerPacUserDynaFlowTypeList)
from .pac_config_dyna_flow_dft_build_to_do_list import (  # noqa: F401
    ReportManagerPacConfigDynaFlowDFTBuildToDoList)
from .pac_config_dyna_flow_retry_task_build_list import (  # noqa: F401
    ReportManagerPacConfigDynaFlowRetryTaskBuildList)
from .pac_config_dyna_flow_task_retry_run_list import (  # noqa: F401
    ReportManagerPacConfigDynaFlowTaskRetryRunList)
from .pac_config_dyna_flow_task_run_to_do_list import (  # noqa: F401
    ReportManagerPacConfigDynaFlowTaskRunToDoList)
from .pac_config_dyna_flow_task_search import (  # noqa: F401
    ReportManagerPacConfigDynaFlowTaskSearch)


from .row_models.tac_farm_dashboard import (  # noqa: F401
    ReportItemTacFarmDashboard)
from .row_models.pac_user_date_greater_than_filter_list import (  # noqa: F401
    ReportItemPacUserDateGreaterThanFilterList)
from .row_models.pac_user_flavor_list import (  # noqa: F401
    ReportItemPacUserFlavorList)
from .row_models.pac_user_land_list import (  # noqa: F401
    ReportItemPacUserLandList)
from .row_models.pac_user_role_list import (  # noqa: F401
    ReportItemPacUserRoleList)
from .row_models.pac_user_tac_list import (  # noqa: F401
    ReportItemPacUserTacList)
from .row_models.pac_user_tri_state_filter_list import (  # noqa: F401
    ReportItemPacUserTriStateFilterList)
from .row_models.plant_user_details import (  # noqa: F401
    ReportItemPlantUserDetails)


from .pac_user_dyna_flow_task_type_list import (  # noqa: F401
    ReportItemPacUserDynaFlowTaskTypeList)
from .pac_user_dyna_flow_type_list import (  # noqa: F401
    ReportItemPacUserDynaFlowTypeList)
from .pac_config_dyna_flow_dft_build_to_do_list import (  # noqa: F401
    ReportItemPacConfigDynaFlowDFTBuildToDoList)
from .pac_config_dyna_flow_retry_task_build_list import (  # noqa: F401
    ReportItemPacConfigDynaFlowRetryTaskBuildList)
from .pac_config_dyna_flow_task_retry_run_list import (  # noqa: F401
    ReportItemPacConfigDynaFlowTaskRetryRunList)
from .pac_config_dyna_flow_task_run_to_do_list import (  # noqa: F401
    ReportItemPacConfigDynaFlowTaskRunToDoList)
from .pac_config_dyna_flow_task_search import (  # noqa: F401
    ReportItemPacConfigDynaFlowTaskSearch)

##GENTrainingBlock[a]End
##GENLOOPObjectEnd
