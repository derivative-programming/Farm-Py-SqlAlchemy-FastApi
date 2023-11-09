##GENLOOPObjectStart
##GENTrainingBlock[a]Start
##GENLearn[modelType=object,name=Land]Start 
##GENLOOPObjectWorkflowStart
##GENTrainingBlock[b]Start
##GENLearn[modelType=objectWorkflow,name=LandAddPlant,calculatedIsInitObjWF=false]Start 
from .land_add_plant import LandAddPlantPostModelRequest,LandAddPlantPostModelResponse
##GENLearn[modelType=objectWorkflow,name=LandAddPlant,calculatedIsInitObjWF=false]End
##GENTrainingBlock[b]End
##GENLOOPObjectWorkflowEnd 
##GENLOOPReportStart
##GENTrainingBlock[b2]Start
##GENLearn[modelType=report,name=LandPlantList]Start 
from .land_plant_list import LandPlantListGetModelRequest,LandPlantListGetModelResponse,LandPlantListGetModelResponseItem
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b2]End
##GENLOOPReportEnd 
##GENLearn[modelType=object,name=Land]End 
from .tac_login import TacLoginPostModelRequest,TacLoginPostModelResponse
from .tac_register import TacRegisterPostModelRequest,TacRegisterPostModelResponse
from .tac_farm_dashboard import TacFarmDashboardGetModelRequest, TacFarmDashboardGetModelResponse, TacFarmDashboardGetModelResponseItem
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
