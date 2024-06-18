# apis/fs_farm_api/v1_0/routers.py

"""
    #TODO add comment
"""

from fastapi import APIRouter
from .endpoints.land_plant_list import LandPlantListRouter
from .endpoints.land_add_plant import LandAddPlantRouter
from .endpoints.customer_user_log_out import CustomerUserLogOutRouter
from .endpoints.pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListRouter
from .endpoints.pac_user_flavor_list import PacUserFlavorListRouter
from .endpoints.pac_user_land_list import PacUserLandListRouter
from .endpoints.pac_user_role_list import PacUserRoleListRouter
from .endpoints.pac_user_tac_list import PacUserTacListRouter
from .endpoints.pac_user_tri_state_filter_list import PacUserTriStateFilterListRouter
from .endpoints.plant_user_details import PlantUserDetailsRouter
from .endpoints.tac_login import TacLoginRouter
from .endpoints.tac_register import TacRegisterRouter
from .endpoints.tac_farm_dashboard import TacFarmDashboardRouter
from .endpoints.plant_user_delete import PlantUserDeleteRouter
from .endpoints.plant_user_property_random_update import PlantUserPropertyRandomUpdateRouter
from .endpoints.customer_build_temp_api_key import CustomerBuildTempApiKeyRouter
from .endpoints.error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogRouter
from .endpoints.land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditableRouter
from .endpoints.land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditableRouter

fs_farm_api_v1_0_router = APIRouter()


def include_all_routers():
    """
    #TODO add comment
    """

    fs_farm_api_v1_0_router.include_router(  # LandPlantList
        LandPlantListRouter.router)
    fs_farm_api_v1_0_router.include_router(  # LandAddPlant
        LandAddPlantRouter.router)
    fs_farm_api_v1_0_router.include_router(  # CustomerUserLogOut
        CustomerUserLogOutRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PacUserDateGreaterThanFilterList
        PacUserDateGreaterThanFilterListRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PacUserFlavorList
        PacUserFlavorListRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PacUserLandList
        PacUserLandListRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PacUserRoleList
        PacUserRoleListRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PacUserTacList
        PacUserTacListRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PacUserTriStateFilterList
        PacUserTriStateFilterListRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PlantUserDetails
        PlantUserDetailsRouter.router)
    fs_farm_api_v1_0_router.include_router(  # TacLogin
        TacLoginRouter.router)
    fs_farm_api_v1_0_router.include_router(  # TacRegister
        TacRegisterRouter.router)
    fs_farm_api_v1_0_router.include_router(  # TacFarmDashboard
        TacFarmDashboardRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PlantUserDelete
        PlantUserDeleteRouter.router)
    fs_farm_api_v1_0_router.include_router(  # PlantUserPropertyRandomUpdate
        PlantUserPropertyRandomUpdateRouter.router)
    fs_farm_api_v1_0_router.include_router(  # CustomerBuildTempApiKey
        CustomerBuildTempApiKeyRouter.router)
    fs_farm_api_v1_0_router.include_router(  # ErrorLogConfigResolveErrorLog
        ErrorLogConfigResolveErrorLogRouter.router)
    fs_farm_api_v1_0_router.include_router(  # LandUserPlantMultiSelectToEditable
        LandUserPlantMultiSelectToEditableRouter.router)
    fs_farm_api_v1_0_router.include_router(  # LandUserPlantMultiSelectToNotEditable
        LandUserPlantMultiSelectToNotEditableRouter.router)


include_all_routers()
