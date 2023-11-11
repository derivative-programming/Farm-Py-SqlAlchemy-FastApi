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
class PacUserDateGreaterThanFilterListRouterConfig():
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
class PacUserDateGreaterThanFilterListRouter(BaseRouter):
    router = APIRouter()

    @staticmethod
    @router.get("/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/init", response_model=api_init_models.PacUserDateGreaterThanFilterListInitReportGetInitModelResponse)
    async def request_get_init(pac_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('PacUserDateGreaterThanFilterListRouter.request_get_init start. pacCode:' + pac_code)
        auth_dict = BaseRouter.implementation_check(PacUserDateGreaterThanFilterListRouterConfig.isGetInitAvailable)
        # if PacUserDateGreaterThanFilterListRouterConfig.isGetInitAvailable == False:
        #     raise HTTPException(
        #         status_code=status.HTTP_501_NOT_IMPLEMENTED,
        #         detail="This method is not implemented.")
        response = api_init_models.PacUserDateGreaterThanFilterListInitReportGetInitModelResponse()
        auth_dict = BaseRouter.authorization_check(PacUserDateGreaterThanFilterListRouterConfig.isPublic, api_key)
        # auth_dict = dict()
        # if PacUserDateGreaterThanFilterListRouterConfig.isPublic == False:
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
                pac_code = session_context.check_context_code("PacCode", pac_code)
                init_request = api_init_models.PacUserDateGreaterThanFilterListInitReportGetInitModelRequest()
                response = await init_request.process_request(
                    session,
                    session_context,
                    pac_code,
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
        logging.info('PacUserDateGreaterThanFilterListRouter.init get result:' + response.model_dump_json())
        return response

    @staticmethod
    @router.get("/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}", response_model=api_models.PacUserDateGreaterThanFilterListGetModelResponse)
    async def request_get_with_id(pac_code: str, request_model:api_models.PacUserDateGreaterThanFilterListGetModelRequest = Depends(),  session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('PacUserDateGreaterThanFilterListRouter.request_get_with_id start. pacCode:' + pac_code)
        auth_dict = BaseRouter.implementation_check(PacUserDateGreaterThanFilterListRouterConfig.isGetWithIdAvailable)
        # if PacUserDateGreaterThanFilterListRouterConfig.isGetWithIdAvailable == False:
        #     raise HTTPException(
        #         status_code=status.HTTP_501_NOT_IMPLEMENTED,
        #         detail="This method is not implemented.")
        response = api_models.PacUserDateGreaterThanFilterListGetModelResponse()
        auth_dict = BaseRouter.authorization_check(PacUserDateGreaterThanFilterListRouterConfig.isPublic, api_key)
        # auth_dict = dict()
        # if PacUserDateGreaterThanFilterListRouterConfig.isPublic == False:
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
                pac_code = session_context.check_context_code("PacCode", pac_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session,
                    session_context,
                    pac_code,
                    request_model
                )
                logging.info('PacUserDateGreaterThanFilterListRouter success')
            except Exception as e:
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success == True:
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('PacUserDateGreaterThanFilterListRouter.submit get result:' + response.model_dump_json())
        return response

    @staticmethod
    @router.get("/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv", response_model=api_models.PacUserDateGreaterThanFilterListGetModelResponse)
    async def request_get_with_id_to_csv(pac_code: str, request_model:api_models.PacUserDateGreaterThanFilterListGetModelRequest = Depends(), session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('PacUserDateGreaterThanFilterListRouter.request_get_with_id_to_csv start. pacCode:' + pac_code)
        auth_dict = BaseRouter.implementation_check(PacUserDateGreaterThanFilterListRouterConfig.isGetToCsvAvailable)
        # if PacUserDateGreaterThanFilterListRouterConfig.isGetToCsvAvailable == False:
        #     raise HTTPException(
        #         status_code=status.HTTP_501_NOT_IMPLEMENTED,
        #         detail="This method is not implemented.")
        response = api_models.PacUserDateGreaterThanFilterListGetModelResponse()
        auth_dict = super().authorization_check(PacUserDateGreaterThanFilterListRouterConfig.isPublic, api_key)
        # auth_dict = dict()
        # if PacUserDateGreaterThanFilterListRouterConfig.isPublic == False:
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
                pac_code = session_context.check_context_code("PacCode", pac_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session,
                    session_context,
                    pac_code,
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
        logging.info('PacUserDateGreaterThanFilterListRouter.submit get result:' + response.model_dump_json())
        return response

