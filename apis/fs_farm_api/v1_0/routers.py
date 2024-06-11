# apis/fs_farm_api/v1_0/routers.py

"""
    #TODO add comment
"""

from fastapi import APIRouter
from .endpoints.land_plant_list import (
    LandPlantListRouter
    )
from .endpoints.land_add_plant import (  # LandAddPlant
    LandAddPlantRouter
    )
from .endpoints.customer_user_log_out import (  # CustomerUserLogOut
    CustomerUserLogOutRouter
    )
from .endpoints.pac_user_date_greater_than_filter_list import (  # PacUserDateGreaterThanFilterList
    PacUserDateGreaterThanFilterListRouter
    )
from .endpoints.pac_user_flavor_list import (  # PacUserFlavorList
    PacUserFlavorListRouter
    )
from .endpoints.pac_user_land_list import (  # PacUserLandList
    PacUserLandListRouter
    )
from .endpoints.pac_user_role_list import (  # PacUserRoleList
    PacUserRoleListRouter
    )
from .endpoints.pac_user_tac_list import (  # PacUserTacList
    PacUserTacListRouter
    )
from .endpoints.pac_user_tri_state_filter_list import (  # PacUserTriStateFilterList
    PacUserTriStateFilterListRouter
    )
from .endpoints.plant_user_details import (  # PlantUserDetails
    PlantUserDetailsRouter
    )
from .endpoints.tac_login import (  # TacLogin
    TacLoginRouter
    )
from .endpoints.tac_register import (  # TacRegister
    TacRegisterRouter
    )
from .endpoints.tac_farm_dashboard import (  # TacFarmDashboard
    TacFarmDashboardRouter
    )
from .endpoints.plant_user_delete import (  # PlantUserDelete
    PlantUserDeleteRouter
    )
from .endpoints.plant_user_property_random_update import (  # PlantUserPropertyRandomUpdate
    PlantUserPropertyRandomUpdateRouter
    )
from .endpoints.customer_build_temp_api_key import (  # CustomerBuildTempApiKey
    CustomerBuildTempApiKeyRouter
    )
from .endpoints.error_log_config_resolve_error_log import (  # ErrorLogConfigResolveErrorLog
    ErrorLogConfigResolveErrorLogRouter
    )
from .endpoints.land_user_plant_multi_select_to_editable import (  # LandUserPlantMultiSelectToEditable
    LandUserPlantMultiSelectToEditableRouter
    )
from .endpoints.land_user_plant_multi_select_to_not_editable import (  # LandUserPlantMultiSelectToNotEditable
    LandUserPlantMultiSelectToNotEditableRouter
    )

fs_farm_api_v1_0_router = APIRouter()

def include_all_routers():

    fs_farm_api_v1_0_router.include_router(LandPlantListRouter.router)  # LandPlantList
    fs_farm_api_v1_0_router.include_router(LandAddPlantRouter.router)  # LandAddPlant
    fs_farm_api_v1_0_router.include_router(CustomerUserLogOutRouter.router)  # CustomerUserLogOut
    fs_farm_api_v1_0_router.include_router(PacUserDateGreaterThanFilterListRouter.router)  # PacUserDateGreaterThanFilterList
    fs_farm_api_v1_0_router.include_router(PacUserFlavorListRouter.router)  # PacUserFlavorList
    fs_farm_api_v1_0_router.include_router(PacUserLandListRouter.router)  # PacUserLandList
    fs_farm_api_v1_0_router.include_router(PacUserRoleListRouter.router)  # PacUserRoleList
    fs_farm_api_v1_0_router.include_router(PacUserTacListRouter.router)  # PacUserTacList
    fs_farm_api_v1_0_router.include_router(PacUserTriStateFilterListRouter.router)  # PacUserTriStateFilterList
    fs_farm_api_v1_0_router.include_router(PlantUserDetailsRouter.router)  # PlantUserDetails
    fs_farm_api_v1_0_router.include_router(TacLoginRouter.router)  # TacLogin
    fs_farm_api_v1_0_router.include_router(TacRegisterRouter.router)  # TacRegister
    fs_farm_api_v1_0_router.include_router(TacFarmDashboardRouter.router)  # TacFarmDashboard
    fs_farm_api_v1_0_router.include_router(PlantUserDeleteRouter.router)  # PlantUserDelete
    fs_farm_api_v1_0_router.include_router(PlantUserPropertyRandomUpdateRouter.router)  # PlantUserPropertyRandomUpdate
    fs_farm_api_v1_0_router.include_router(CustomerBuildTempApiKeyRouter.router)  # CustomerBuildTempApiKey
    fs_farm_api_v1_0_router.include_router(ErrorLogConfigResolveErrorLogRouter.router)  # ErrorLogConfigResolveErrorLog
    fs_farm_api_v1_0_router.include_router(LandUserPlantMultiSelectToEditableRouter.router)  # LandUserPlantMultiSelectToEditable
    fs_farm_api_v1_0_router.include_router(LandUserPlantMultiSelectToNotEditableRouter.router)  # LandUserPlantMultiSelectToNotEditable

include_all_routers()
