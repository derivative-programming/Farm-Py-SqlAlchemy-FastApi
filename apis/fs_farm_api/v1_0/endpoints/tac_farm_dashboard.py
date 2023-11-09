from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
import traceback
import logging
from helpers import SessionContext, ApiToken, api_key_header
import apis.models.init as api_init_models
import apis.models as api_models
from database import get_db
class TacFarmDashboardRouterConfig():
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
class TacFarmDashboardRouter():
    router = APIRouter()

    @staticmethod
    @router.get("/api/v1_0/tac-farm-dashboard/{tac_code}/init", response_model=api_init_models.TacFarmDashboardInitReportGetInitModelResponse)
    async def request_get_init(tac_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.debug('TacFarmDashboardRouter.request_get_init start. tacCode:' + tac_code)
        if TacFarmDashboardRouterConfig.isGetInitAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="This method is not implemented.")
        response = api_init_models.TacFarmDashboardInitReportGetInitModelResponse()
        auth_dict = dict()
        if TacFarmDashboardRouterConfig.isPublic == False:
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
                tac_code = session_context.check_context_code("TacCode", tac_code)
                init_request = api_init_models.TacFarmDashboardInitReportGetInitModelRequest()
                response = await init_request.process_request(
                    session,
                    session_context,
                    tac_code,
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
        logging.debug('TacFarmDashboardRouter.init get result:' + response.to_json())
        return response

    @staticmethod
    @router.get("/api/v1_0/tac-farm-dashboard/{tac_code}", response_model=api_models.TacFarmDashboardGetModelResponse)
    async def request_get_with_id(tac_code: str, request_model:api_models.TacFarmDashboardGetModelRequest, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.debug('TacFarmDashboardRouter.request_get_with_id start. tacCode:' + tac_code)
        if TacFarmDashboardRouterConfig.isGetWithIdAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="This method is not implemented.")
        response = api_models.TacFarmDashboardGetModelResponse()
        auth_dict = dict()
        if TacFarmDashboardRouterConfig.isPublic == False:
            auth_dict = ApiToken.validate_token(api_key)
            if auth_dict == None or len(auth_dict) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized.")
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict)
                tac_code = session_context.check_context_code("TacCode", tac_code)
                response.request = request
                logging.debug("process request...")
                await response.process_request(
                    session,
                    session_context,
                    tac_code,
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
        logging.debug('TacFarmDashboardRouter.submit get result:' + response.to_json())
        return response

    @staticmethod
    @router.get("/api/v1_0/tac-farm-dashboard/{tac_code}/to-csv", response_model=api_models.TacFarmDashboardGetModelResponse)
    async def request_get_with_id_to_csv(tac_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.debug('TacFarmDashboardRouter.request_get_with_id_to_csv start. tacCode:' + tac_code)
        if TacFarmDashboardRouterConfig.isGetToCsvAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="This method is not implemented.")
        response = api_models.TacFarmDashboardGetModelResponse()
        auth_dict = dict()
        if TacFarmDashboardRouterConfig.isPublic == False:
            auth_dict = ApiToken.validate_token(api_key)
            if auth_dict == None or len(auth_dict) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized.")
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict)
                tac_code = session_context.check_context_code("TacCode", tac_code)
                response.request = request_model
                logging.debug("process request...")
                await response.process_request(
                    session,
                    session_context,
                    tac_code,
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
        logging.debug('TacFarmDashboardRouter.submit get result:' + response.to_json())
        return response

