# apis/models/__init__.py

"""
    #TODO add comment
"""

##GENLOOPObjectStart
##GENTrainingBlock[a]Start
##GENLearn[modelType=object,name=Land]Start
##GENLOOPObjectWorkflowStart
##GENTrainingBlock[b]Start
##GENLearn[modelType=objectWorkflow,name=LandAddPlant,calculatedIsInitObjWF=false]Start
from .land_add_plant import (
    LandAddPlantPostModelRequest,
    LandAddPlantPostModelResponse)
##GENLearn[modelType=objectWorkflow,name=LandAddPlant,calculatedIsInitObjWF=false]End
##GENTrainingBlock[b]End
##GENLOOPObjectWorkflowEnd
##GENLOOPReportStart
##GENTrainingBlock[b2]Start
##GENLearn[modelType=report,name=LandPlantList]Start
from .land_plant_list import (
    LandPlantListGetModelRequest,
    LandPlantListGetModelResponse,
    LandPlantListGetModelResponseItem)
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b2]End
##GENLOOPReportEnd
##GENLearn[modelType=object,name=Land]End
from .tac_login import (
    TacLoginPostModelRequest,
    TacLoginPostModelResponse)
from .tac_register import (
    TacRegisterPostModelRequest,
    TacRegisterPostModelResponse)
from .tac_farm_dashboard import (
    TacFarmDashboardGetModelRequest,
    TacFarmDashboardGetModelResponse,
    TacFarmDashboardGetModelResponseItem)
from .customer_build_temp_api_key import (
    CustomerBuildTempApiKeyPostModelRequest,
    CustomerBuildTempApiKeyPostModelResponse)
from .customer_user_log_out import (
    CustomerUserLogOutPostModelRequest,
    CustomerUserLogOutPostModelResponse)
from .error_log_config_resolve_error_log import (
    ErrorLogConfigResolveErrorLogPostModelRequest,
    ErrorLogConfigResolveErrorLogPostModelResponse)
from .land_user_plant_multi_select_to_editable import (
    LandUserPlantMultiSelectToEditablePostModelRequest,
    LandUserPlantMultiSelectToEditablePostModelResponse)
from .land_user_plant_multi_select_to_not_editable import (
    LandUserPlantMultiSelectToNotEditablePostModelRequest,
    LandUserPlantMultiSelectToNotEditablePostModelResponse)
from .pac_user_date_greater_than_filter_list import (
    PacUserDateGreaterThanFilterListGetModelRequest,
    PacUserDateGreaterThanFilterListGetModelResponse,
    PacUserDateGreaterThanFilterListGetModelResponseItem)
from .pac_user_flavor_list import (
    PacUserFlavorListGetModelRequest,
    PacUserFlavorListGetModelResponse,
    PacUserFlavorListGetModelResponseItem)
from .pac_user_land_list import (
    PacUserLandListGetModelRequest,
    PacUserLandListGetModelResponse,
    PacUserLandListGetModelResponseItem)
from .pac_user_role_list import (
    PacUserRoleListGetModelRequest,
    PacUserRoleListGetModelResponse,
    PacUserRoleListGetModelResponseItem)
from .pac_user_tac_list import (
    PacUserTacListGetModelRequest,
    PacUserTacListGetModelResponse,
    PacUserTacListGetModelResponseItem)
from .pac_user_tri_state_filter_list import (
    PacUserTriStateFilterListGetModelRequest,
    PacUserTriStateFilterListGetModelResponse,
    PacUserTriStateFilterListGetModelResponseItem)
from .plant_user_delete import (
    PlantUserDeletePostModelRequest,
    PlantUserDeletePostModelResponse)
from .plant_user_details import (
    PlantUserDetailsGetModelRequest,
    PlantUserDetailsGetModelResponse,
    PlantUserDetailsGetModelResponseItem)
from .plant_user_property_random_update import (
    PlantUserPropertyRandomUpdatePostModelRequest,
    PlantUserPropertyRandomUpdatePostModelResponse)
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
