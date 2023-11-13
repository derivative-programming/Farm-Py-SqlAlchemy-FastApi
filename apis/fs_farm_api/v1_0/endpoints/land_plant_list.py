import tempfile
import uuid
from fastapi import APIRouter, Depends 
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import traceback  
import logging 
from helpers import SessionContext, api_key_header
import apis.models.init as api_init_models
import apis.models as api_models 
import reports
from  .base_router import BaseRouter
from database import get_db 

class LandPlantListRouterConfig():
    #constants
    is_get_available:bool = False
    is_get_with_id_available:bool = True
    is_get_init_available:bool = True
    is_get_to_csv_available:bool = True
    is_post_available:bool = False
    is_post_with_id_available:bool = False
    is_put_available:bool = False 
    is_delete_available:bool = False  
    is_public: bool = False 

class LandPlantListRouter(BaseRouter):   
    router = APIRouter()
     
##GENTrainingBlock[caseisGetInitAvailable]Start
##GENLearn[isGetInitAvailable=true]Start
    @staticmethod
    @router.get("/api/v1_0/land-plant-list/{land_code}/init", response_model=api_init_models.LandPlantListInitReportGetInitModelResponse)  
    async def request_get_init(land_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('LandPlantListRouter.request_get_init start. landCode:' + land_code)
        auth_dict = BaseRouter.implementation_check(LandPlantListRouterConfig.is_get_init_available)
        
        response = api_init_models.LandPlantListInitReportGetInitModelResponse() 

        auth_dict = BaseRouter.authorization_check(LandPlantListRouterConfig.is_public, api_key) 
            
        # Start a transaction
        async with session:
            try: 
                logging.info("Start session...")
                session_context = SessionContext(auth_dict)
                land_code = session_context.check_context_code("LandCode", land_code)
                init_request = api_init_models.LandPlantListInitReportGetInitModelRequest() 
                response = await init_request.process_request(
                    session,
                    session_context,
                    land_code,
                    response
                )  
            except TypeError as te: 
                response.success = False
                traceback_string = "".join(traceback.format_tb(te.__traceback__))
                response.message = str(te) + " traceback:" + traceback_string 
            except Exception as e:
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success == True:
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('LandPlantListRouter.init get result:' + response.model_dump_json()) 
        return response
##GENLearn[isGetInitAvailable=true]End
##GENTrainingBlock[caseisGetInitAvailable]End 
##GENTrainingBlock[caseisGetAvailable]Start
##GENLearn[isGetAvailable=false]Start 
##GENLearn[isGetAvailable=false]End
##GENTrainingBlock[caseisGetAvailable]End 
##GENTrainingBlock[caseisGetWithIdAvailable]Start 
##GENLearn[isGetWithIdAvailable=true]Start
    @staticmethod
    @router.get("/api/v1_0/land-plant-list/{land_code}", response_model=api_models.LandPlantListGetModelResponse)
    async def request_get_with_id(land_code: str, request_model:api_models.LandPlantListGetModelRequest = Depends(),  session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)): 
        logging.info('LandPlantListRouter.request_get_with_id start. landCode:' + land_code)
        auth_dict = BaseRouter.implementation_check(LandPlantListRouterConfig.is_get_with_id_available)
        
        response = api_models.LandPlantListGetModelResponse()
 
        auth_dict = BaseRouter.authorization_check(LandPlantListRouterConfig.is_public, api_key) 
            
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict)
                land_code = session_context.check_context_code("LandCode", land_code) 
                logging.info("Request...") 
                logging.info(request_model.__dict__) 
                response.request = request_model
                logging.info("process request...") 
                await response.process_request(
                    session,
                    session_context,
                    land_code,
                    request_model
                )   
                logging.info('LandPlantListRouter success')
            except Exception as e:
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success == True:
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('LandPlantListRouter.submit get result:' + response.model_dump_json())
        return response
##GENLearn[isGetWithIdAvailable=true]End
##GENTrainingBlock[caseisGetWithIdAvailable]End
##GENTrainingBlock[caseisGetToCsvAvailable]Start 
##GENLearn[isGetToCsvAvailable=true]Start
    @staticmethod
    @router.get("/api/v1_0/land-plant-list/{land_code}/to-csv", response_class=FileResponse) 
    async def request_get_with_id_to_csv(land_code: str, request_model:api_models.LandPlantListGetModelRequest = Depends(), session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('LandPlantListRouter.request_get_with_id_to_csv start. landCode:' + land_code)
        auth_dict = BaseRouter.implementation_check(LandPlantListRouterConfig.is_get_to_csv_available)
        
        response = api_models.LandPlantListGetModelResponse()

        auth_dict = super().authorization_check(LandPlantListRouterConfig.is_public, api_key) 
            
        tmp_file_path = "" 
        
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv', encoding='utf-8') as tmp_file:
            tmp_file_path = tmp_file.name

        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict)
                land_code = session_context.check_context_code("LandCode", land_code) 
                logging.info("Request...") 
                logging.info(request_model.__dict__) 
                response.request = request_model
                logging.info("process request...") 
                await response.process_request(
                    session,
                    session_context,
                    land_code,
                    request_model
                ) 
                report_manager = reports.ReportManagerLandPlantList(session,session_context)
                report_manager.build_csv(tmp_file_path,response.items)
            except Exception as e:
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success == True:
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('LandPlantListRouter.submit get result:' + response.model_dump_json()) 
        output_file_name = 'land_plant_list_' + land_code + '_' + str(uuid.UUID()) + '.csv'
        return FileResponse(tmp_file_path, media_type='text/csv', filename=output_file_name)

##GENLearn[isGetToCsvAvailable=true]End
##GENTrainingBlock[caseisGetToCsvAvailable]End 
##GENTrainingBlock[caseisPostAvailable]Start
##GENLearn[isPostAvailable=false]Start 
##GENLearn[isPostAvailable=false]End
##GENTrainingBlock[caseisPostAvailable]End
##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=false]Start 
##GENLearn[isPostWithIdAvailable=false]End
##GENTrainingBlock[caseisPostWithIdAvailable]End
##GENTrainingBlock[caseisPutAvailable]Start
##GENLearn[isPutAvailable=false]Start 
##GENLearn[isPutAvailable=false]End
##GENTrainingBlock[caseisPutAvailable]End
##GENTrainingBlock[caseisDeleteAvailable]Start
##GENLearn[isDeleteAvailable=false]Start 
##GENLearn[isDeleteAvailable=false]End
##GENTrainingBlock[caseisDeleteAvailable]End
