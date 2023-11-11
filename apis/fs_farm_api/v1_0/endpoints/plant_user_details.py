from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
import traceback
import logging
from helpers import SessionContext, ApiToken, api_key_header
import apis.models.init as api_init_models
import apis.models as api_models
from  .base_router import BaseRouter
from database import get_db
class PlantUserDetailsRouterConfig():
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
class PlantUserDetailsRouter(BaseRouter):
    router = APIRouter()

    @staticmethod
    @router.get("/api/v1_0/plant-user-details/{plant_code}/init", response_model=api_init_models.PlantUserDetailsInitReportGetInitModelResponse)
    async def request_get_init(plant_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('PlantUserDetailsRouter.request_get_init start. plantCode:' + plant_code)
        auth_dict = BaseRouter.implementation_check(PlantUserDetailsRouterConfig.isGetInitAvailable)
        # if PlantUserDetailsRouterConfig.isGetInitAvailable == False:
        #     raise HTTPException(
        #         status_code=status.HTTP_501_NOT_IMPLEMENTED,
        #         detail="This method is not implemented.")
        response = api_init_models.PlantUserDetailsInitReportGetInitModelResponse()
        auth_dict = BaseRouter.authorization_check(PlantUserDetailsRouterConfig.isPublic, api_key)
        # auth_dict = dict()
        # if PlantUserDetailsRouterConfig.isPublic == False:
        #     logging.info("Authorization Required...")
        #     auth_dict = ApiToken.validate_token(api_key)
        #     if auth_dict == None or len(auth_dict) == 0:
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="Unauthorized.")
        #     logging.info("auth_dict:" + str(auth_dict))
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict)
                plant_code = session_context.check_context_code("PlantCode", plant_code)
                init_request = api_init_models.PlantUserDetailsInitReportGetInitModelRequest()
                response = await init_request.process_request(
                    session,
                    session_context,
                    plant_code,
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
        logging.info('PlantUserDetailsRouter.init get result:' + response.model_dump_json())
        return response

    @staticmethod
    @router.get("/api/v1_0/plant-user-details/{plant_code}", response_model=api_models.PlantUserDetailsGetModelResponse)
    async def request_get_with_id(plant_code: str, request_model:api_models.PlantUserDetailsGetModelRequest = Depends(),  session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('PlantUserDetailsRouter.request_get_with_id start. plantCode:' + plant_code)
        auth_dict = BaseRouter.implementation_check(PlantUserDetailsRouterConfig.isGetWithIdAvailable)
        # if PlantUserDetailsRouterConfig.isGetWithIdAvailable == False:
        #     raise HTTPException(
        #         status_code=status.HTTP_501_NOT_IMPLEMENTED,
        #         detail="This method is not implemented.")
        response = api_models.PlantUserDetailsGetModelResponse()
        auth_dict = BaseRouter.authorization_check(PlantUserDetailsRouterConfig.isPublic, api_key)
        # auth_dict = dict()
        # if PlantUserDetailsRouterConfig.isPublic == False:
        #     logging.info("Authorization Required...")
        #     auth_dict = ApiToken.validate_token(api_key)
        #     if auth_dict == None or len(auth_dict) == 0:
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="Unauthorized.")
        #     logging.info("auth_dict:" + str(auth_dict))
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict)
                plant_code = session_context.check_context_code("PlantCode", plant_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session,
                    session_context,
                    plant_code,
                    request_model
                )
                logging.info('PlantUserDetailsRouter success')
            except Exception as e:
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success == True:
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('PlantUserDetailsRouter.submit get result:' + response.model_dump_json())
        return response

    @staticmethod
    @router.get("/api/v1_0/plant-user-details/{plant_code}/to-csv", response_model=api_models.PlantUserDetailsGetModelResponse)
    async def request_get_with_id_to_csv(plant_code: str, request_model:api_models.PlantUserDetailsGetModelRequest = Depends(), session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('PlantUserDetailsRouter.request_get_with_id_to_csv start. plantCode:' + plant_code)
        auth_dict = BaseRouter.implementation_check(PlantUserDetailsRouterConfig.isGetToCsvAvailable)
        # if PlantUserDetailsRouterConfig.isGetToCsvAvailable == False:
        #     raise HTTPException(
        #         status_code=status.HTTP_501_NOT_IMPLEMENTED,
        #         detail="This method is not implemented.")
        response = api_models.PlantUserDetailsGetModelResponse()
        auth_dict = super().authorization_check(PlantUserDetailsRouterConfig.isPublic, api_key)
        # auth_dict = dict()
        # if PlantUserDetailsRouterConfig.isPublic == False:
        #     logging.info("Authorization Required...")
        #     auth_dict = ApiToken.validate_token(api_key)
        #     if auth_dict == None or len(auth_dict) == 0:
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="Unauthorized.")
        #     logging.info("auth_dict:" + str(auth_dict))
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict)
                plant_code = session_context.check_context_code("PlantCode", plant_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session,
                    session_context,
                    plant_code,
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
        logging.info('PlantUserDetailsRouter.submit get result:' + response.model_dump_json())
        return response

