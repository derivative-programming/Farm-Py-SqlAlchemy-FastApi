# apis/models/__init__.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import


"""
This module contains the model classes for the API.

The models in this module represent the data
structures used in the API endpoints.
"""

##GENLOOPObjectStart
##GENTrainingBlock[a]Start
##GENLearn[modelType=object,name=Land]Start
##GENLOOPObjectWorkflowStart
##GENTrainingBlock[b]Start
##GENLearn[modelType=objectWorkflow,name=LandAddPlant,calculatedIsInitObjWF=false]Start
from .land_add_plant import (  # noqa: F401
    LandAddPlantPostModelRequest,
    LandAddPlantPostModelResponse)
##GENLearn[modelType=objectWorkflow,name=LandAddPlant,calculatedIsInitObjWF=false]End
##GENTrainingBlock[b]End
##GENLOOPObjectWorkflowEnd
##GENLOOPReportStart
##GENTrainingBlock[b2]Start
##GENLearn[modelType=report,name=LandPlantList]Start
from .land_plant_list import (  # noqa: F401
    LandPlantListGetModelRequest,
    LandPlantListGetModelResponse,
    LandPlantListGetModelResponseItem)
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b2]End
##GENLOOPReportEnd
##GENLearn[modelType=object,name=Land]End
from .tac_login import (  # noqa: F401
    TacLoginPostModelRequest,
    TacLoginPostModelResponse)
from .tac_register import (  # noqa: F401
    TacRegisterPostModelRequest,
    TacRegisterPostModelResponse)
from .tac_farm_dashboard import (  # noqa: F401
    TacFarmDashboardGetModelRequest,
    TacFarmDashboardGetModelResponse,
    TacFarmDashboardGetModelResponseItem)
from .customer_build_temp_api_key import (  # noqa: F401
    CustomerBuildTempApiKeyPostModelRequest,
    CustomerBuildTempApiKeyPostModelResponse)
from .customer_user_log_out import (  # noqa: F401
    CustomerUserLogOutPostModelRequest,
    CustomerUserLogOutPostModelResponse)
from .error_log_config_resolve_error_log import (  # noqa: F401
    ErrorLogConfigResolveErrorLogPostModelRequest,
    ErrorLogConfigResolveErrorLogPostModelResponse)
from .land_user_plant_multi_select_to_editable import (  # noqa: F401
    LandUserPlantMultiSelectToEditablePostModelRequest,
    LandUserPlantMultiSelectToEditablePostModelResponse)
from .land_user_plant_multi_select_to_not_editable import (  # noqa: F401
    LandUserPlantMultiSelectToNotEditablePostModelRequest,
    LandUserPlantMultiSelectToNotEditablePostModelResponse)
from .pac_user_date_greater_than_filter_list import (  # noqa: F401
    PacUserDateGreaterThanFilterListGetModelRequest,
    PacUserDateGreaterThanFilterListGetModelResponse,
    PacUserDateGreaterThanFilterListGetModelResponseItem)
from .pac_user_flavor_list import (  # noqa: F401
    PacUserFlavorListGetModelRequest,
    PacUserFlavorListGetModelResponse,
    PacUserFlavorListGetModelResponseItem)
from .pac_user_land_list import (  # noqa: F401
    PacUserLandListGetModelRequest,
    PacUserLandListGetModelResponse,
    PacUserLandListGetModelResponseItem)
from .pac_user_role_list import (  # noqa: F401
    PacUserRoleListGetModelRequest,
    PacUserRoleListGetModelResponse,
    PacUserRoleListGetModelResponseItem)
from .pac_user_tac_list import (  # noqa: F401
    PacUserTacListGetModelRequest,
    PacUserTacListGetModelResponse,
    PacUserTacListGetModelResponseItem)
from .pac_user_tri_state_filter_list import (  # noqa: F401
    PacUserTriStateFilterListGetModelRequest,
    PacUserTriStateFilterListGetModelResponse,
    PacUserTriStateFilterListGetModelResponseItem)
from .plant_user_delete import (  # noqa: F401
    PlantUserDeletePostModelRequest,
    PlantUserDeletePostModelResponse)
from .plant_user_details import (  # noqa: F401
    PlantUserDetailsGetModelRequest,
    PlantUserDetailsGetModelResponse,
    PlantUserDetailsGetModelResponseItem)
from .plant_user_property_random_update import (  # noqa: F401
    PlantUserPropertyRandomUpdatePostModelRequest,
    PlantUserPropertyRandomUpdatePostModelResponse)
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
