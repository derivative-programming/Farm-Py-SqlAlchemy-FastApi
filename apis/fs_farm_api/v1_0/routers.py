# routers.py
from fastapi import APIRouter 
from .endpoints.land_plant_list import LandPlantListRouter 
from .endpoints.land_add_plant import LandAddPlantRouter #LandAddPlant
from .endpoints.customer_user_log_out import CustomerUserLogOutRouter #CustomerUserLogOut
from .endpoints.pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListRouter #PacUserDateGreaterThanFilterList
from .endpoints.pac_user_flavor_list import PacUserFlavorListRouter #PacUserFlavorList
from .endpoints.pac_user_land_list import PacUserLandListRouter #PacUserLandList
from .endpoints.pac_user_role_list import PacUserRoleListRouter #PacUserRoleList
from .endpoints.pac_user_tac_list import PacUserTacListRouter #PacUserTacList
from .endpoints.pac_user_tri_state_filter_list import PacUserTriStateFilterListRouter #PacUserTriStateFilterList
from .endpoints.plant_user_details import PlantUserDetailsRouter #PlantUserDetails
from .endpoints.tac_login import TacLoginRouter #TacLogin
from .endpoints.tac_register import TacRegisterRouter #TacRegister
from .endpoints.tac_farm_dashboard import TacFarmDashboardRouter #TacFarmDashboard
from .endpoints.plant_user_delete import PlantUserDeleteRouter #PlantUserDelete
from .endpoints.plant_user_property_random_update import PlantUserPropertyRandomUpdateRouter #PlantUserPropertyRandomUpdate
from .endpoints.customer_build_temp_api_key import CustomerBuildTempApiKeyRouter #CustomerBuildTempApiKey
from .endpoints.error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogRouter #ErrorLogConfigResolveErrorLog
from .endpoints.land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditableRouter #LandUserPlantMultiSelectToEditable
from .endpoints.land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditableRouter #LandUserPlantMultiSelectToNotEditable
 
fs_farm_api_v1_0_router = APIRouter()

def include_all_routers():

    fs_farm_api_v1_0_router.include_router(LandPlantListRouter.router) #LandPlantList
    fs_farm_api_v1_0_router.include_router(LandAddPlantRouter.router) #LandAddPlant
    fs_farm_api_v1_0_router.include_router(CustomerUserLogOutRouter.router) #CustomerUserLogOut
    fs_farm_api_v1_0_router.include_router(PacUserDateGreaterThanFilterListRouter.router) #PacUserDateGreaterThanFilterList
    fs_farm_api_v1_0_router.include_router(PacUserFlavorListRouter.router) #PacUserFlavorList
    fs_farm_api_v1_0_router.include_router(PacUserLandListRouter.router) #PacUserLandList
    fs_farm_api_v1_0_router.include_router(PacUserRoleListRouter.router) #PacUserRoleList
    fs_farm_api_v1_0_router.include_router(PacUserTacListRouter.router) #PacUserTacList
    fs_farm_api_v1_0_router.include_router(PacUserTriStateFilterListRouter.router) #PacUserTriStateFilterList
    fs_farm_api_v1_0_router.include_router(PlantUserDetailsRouter.router) #PlantUserDetails
    fs_farm_api_v1_0_router.include_router(TacLoginRouter.router) #TacLogin
    fs_farm_api_v1_0_router.include_router(TacRegisterRouter.router) #TacRegister
    fs_farm_api_v1_0_router.include_router(TacFarmDashboardRouter.router) #TacFarmDashboard
    fs_farm_api_v1_0_router.include_router(PlantUserDeleteRouter.router) #PlantUserDelete
    fs_farm_api_v1_0_router.include_router(PlantUserPropertyRandomUpdateRouter.router) #PlantUserPropertyRandomUpdate
    fs_farm_api_v1_0_router.include_router(CustomerBuildTempApiKeyRouter.router) #CustomerBuildTempApiKey
    fs_farm_api_v1_0_router.include_router(ErrorLogConfigResolveErrorLogRouter.router) #ErrorLogConfigResolveErrorLog
    fs_farm_api_v1_0_router.include_router(LandUserPlantMultiSelectToEditableRouter.router) #LandUserPlantMultiSelectToEditable
    fs_farm_api_v1_0_router.include_router(LandUserPlantMultiSelectToNotEditableRouter.router) #LandUserPlantMultiSelectToNotEditable
 
include_all_routers()