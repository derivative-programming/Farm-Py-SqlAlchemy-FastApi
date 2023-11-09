from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import APIKeyHeader 
from sqlalchemy.ext.asyncio import AsyncSession
import traceback  
import logging 
from helpers import SessionContext, ApiToken, api_key_header
import apis.models.init as api_init_models
import apis.models as api_models 
from database import get_db
 
router = APIRouter()

logging.basicConfig(level=logging.DEBUG)

class LandAddPlantRouterConfig():
    #constants
    isGetAvailable:bool = False
    isGetWithIdAvailable:bool = False
    isGetInitAvailable:bool = True
    isGetToCsvAvailable:bool = False
    isPostAvailable:bool = False
    isPostWithIdAvailable:bool = True
    isPutAvailable:bool = False 
    isDeleteAvailable:bool = False  
    isPublic: bool = False 

class LandAddPlantRouter():    
    router = APIRouter() 


    @staticmethod
    @router.get("/api/v1_0/land-add-plant/{land_code}/init", response_model=api_init_models.LandAddPlantInitObjWFGetInitModelResponse)
    async def request_get_init(land_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.debug('LandAddPlantRouter.request_get_init start. tacCode:' + land_code)
        if LandAddPlantRouterConfig.isGetInitAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="This method is not implemented.")
        response = api_init_models.LandAddPlantInitObjWFGetInitModelResponse()
        auth_dict = dict()
        if LandAddPlantRouterConfig.isPublic == True:
            auth_dict = ApiToken.validate_token(api_key)
            if auth_dict == None or len(auth_dict) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized.")
        # Start a transaction
        async with session:
            try:
                logging.debug("Start session...")
                session_context = SessionContext(auth_dict)
                land_code = session_context.check_context_code("LandCode", land_code)
                init_request = api_init_models.LandAddPlantInitObjWFGetInitModelRequest()
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
        logging.debug('LandAddPlantRouter.init get result:' + response.to_json())
        return response

##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=true]Start
    @staticmethod
    @router.post("/api/v1_0/land-add-plant/{land_code}", response_model=api_models.LandAddPlantPostModelResponse) 
    async def request_post_with_id(land_code: str, request_model:api_models.LandAddPlantPostModelRequest, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)): 
        logging.debug('LandAddPlantRouter.request_post_with_id start. landCode:' + land_code)
        if LandAddPlantRouterConfig.isPostWithIdAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED, 
                detail="This method is not implemented.") 
        response = api_models.LandAddPlantPostModelResponse()

        auth_dict = dict()
        if LandAddPlantRouterConfig.isPublic == False:
            auth_dict = ApiToken.validate_token(api_key)
            if auth_dict == None or len(auth_dict) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Unauthorized.")      
            
        # Start a transaction
        async with session:
            try:
                logging.debug("Start session...") 
                session_context = SessionContext(auth_dict)
                land_code = session_context.check_context_code("LandCode", land_code)  
                await response.process_request(
                    session,
                    session_context,
                    land_code,
                    request_model
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
        logging.debug('LandAddPlantRouter.submit get result:' + response.to_json()) 
        return response
##GENLearn[isPostWithIdAvailable=true]End
##GENTrainingBlock[caseisPostWithIdAvailable]End  
 