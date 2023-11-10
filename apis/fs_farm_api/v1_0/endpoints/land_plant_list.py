from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import APIKeyHeader 
from sqlalchemy.ext.asyncio import AsyncSession
import traceback  
import logging 
from helpers import SessionContext, ApiToken, api_key_header
import apis.models.init as api_init_models
import apis.models as api_models 
from database import get_db
  
class LandPlantListRouterConfig():
    #constants
    isGetAvailable:bool = False
    isGetWithIdAvailable:bool = True
    isGetInitAvailable:bool = True
    isGetToCsvAvailable:bool = True
    isPostAvailable:bool = False
    isPostWithIdAvailable:bool = False
    isPutAvailable:bool = False 
    isDeleteAvailable:bool = False  
    isPublic: bool = False 

class LandPlantListRouter():   
    router = APIRouter()
    
##GENTrainingBlock[caseisGetInitAvailable]Start
##GENLearn[isGetInitAvailable=true]Start
    @staticmethod
    @router.get("/api/v1_0/land-plant-list/{land_code}/init", response_model=api_init_models.LandPlantListInitReportGetInitModelResponse)  
    async def request_get_init(land_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('LandPlantListRouter.request_get_init start. landCode:' + land_code)
        if LandPlantListRouterConfig.isGetInitAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED, 
                detail="This method is not implemented.") 
        
        response = api_init_models.LandPlantListInitReportGetInitModelResponse() 

        auth_dict = dict()
        if LandPlantListRouterConfig.isPublic == False: 
            logging.info("Authorization Required...") 
            auth_dict = ApiToken.validate_token(api_key)
            if auth_dict == None or len(auth_dict) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Unauthorized.")    
            logging.info("auth_dict:" + str(auth_dict))
            
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
    async def request_get_with_id(land_code: str,  session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)): 
        logging.info('LandPlantListRouter.request_get_with_id start. landCode:' + land_code)
        if LandPlantListRouterConfig.isGetWithIdAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED, 
                detail="This method is not implemented.") 
        response = api_models.LandPlantListGetModelResponse()
 
        auth_dict = dict()
        if LandPlantListRouterConfig.isPublic == False: 
            logging.info("Authorization Required...") 
            auth_dict = ApiToken.validate_token(api_key)
            if auth_dict == None or len(auth_dict) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Unauthorized.")    
            logging.info("auth_dict:" + str(auth_dict))
            
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
    @router.get("/api/v1_0/land-plant-list/{land_code}/to-csv", response_model=api_models.LandPlantListGetModelResponse) 
    async def request_get_with_id_to_csv(land_code: str, request_model:api_models.LandPlantListGetModelRequest = Depends(), session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('LandPlantListRouter.request_get_with_id_to_csv start. landCode:' + land_code)
        if LandPlantListRouterConfig.isGetToCsvAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED, 
                detail="This method is not implemented.") 
        response = api_models.LandPlantListGetModelResponse()

        auth_dict = dict()
        if LandPlantListRouterConfig.isPublic == False: 
            logging.info("Authorization Required...") 
            auth_dict = ApiToken.validate_token(api_key)
            if auth_dict == None or len(auth_dict) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Unauthorized.")    
            logging.info("auth_dict:" + str(auth_dict))
            
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
