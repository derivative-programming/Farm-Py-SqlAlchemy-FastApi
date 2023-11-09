# routers.py
from fastapi import APIRouter
import endpoints as end_point_routers
from endpoints.land_plant_list import LandPlantListRouter #LandPlantList
from endpoints.land_add_plant import LandAddPlantRouter #LandAddPlant
    #CustomerUserLogOut
    #PacUserDateGreaterThanFilterList
    #PacUserFlavorList
    #PacUserLandList
    #PacUserRoleList
    #PacUserTacList
    #PacUserTriStateFilterList
    #PlantUserDetails
    #TacLogin
    #TacRegister
    #TacFarmDashboard
    #PlantUserDelete
    #PlantUserPropertyRandomUpdate
    #CustomerBuildTempApiKey
    #ErrorLogConfigResolveErrorLog
    #LandUserPlantMultiSelectToEditable
    #LandUserPlantMultiSelectToNotEditable

# Create an APIRouter instance which will include all the other routers
fs_farm_api_v1_0_router = APIRouter()

def include_all_routers():

    fs_farm_api_v1_0_router.include_router(LandPlantListRouter.router) #LandPlantList
    fs_farm_api_v1_0_router.include_router(LandAddPlantRouter.router) #LandAddPlant
    #CustomerUserLogOut
    #PacUserDateGreaterThanFilterList
    #PacUserFlavorList
    #PacUserLandList
    #PacUserRoleList
    #PacUserTacList
    #PacUserTriStateFilterList
    #PlantUserDetails
    #TacLogin
    #TacRegister
    #TacFarmDashboard
    #PlantUserDelete
    #PlantUserPropertyRandomUpdate
    #CustomerBuildTempApiKey
    #ErrorLogConfigResolveErrorLog
    #LandUserPlantMultiSelectToEditable
    #LandUserPlantMultiSelectToNotEditable

    

# Call the function to include all routers
include_all_routers()