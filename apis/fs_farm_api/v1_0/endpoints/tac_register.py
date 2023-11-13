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
class TacRegisterRouterConfig():
    #constants
    is_get_available:bool = False
    is_get_with_id_available:bool = False
    is_get_init_available:bool = True
    is_get_to_csv_available:bool = False
    is_post_available:bool = False
    is_post_with_id_available:bool = True
    is_put_available:bool = False
    is_delete_available:bool = False
    is_public: bool = True
class TacRegisterRouter(BaseRouter):
    router = APIRouter()

    @staticmethod
    @router.get("/api/v1_0/tac-register/{tac_code}/init", response_model=api_init_models.TacRegisterInitObjWFGetInitModelResponse)
    async def request_get_init(tac_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('TacRegisterRouter.request_get_init start. tacCode:' + tac_code)
        auth_dict = BaseRouter.implementation_check(TacRegisterRouterConfig.is_get_init_available)
        response = api_init_models.TacRegisterInitObjWFGetInitModelResponse()
        auth_dict = BaseRouter.authorization_check(TacRegisterRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict)
                tac_code = session_context.check_context_code("TacCode", tac_code)
                init_request = api_init_models.TacRegisterInitObjWFGetInitModelRequest()
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
        logging.info('TacRegisterRouter.init get result:' + response.model_dump_json())
        return response

    @staticmethod
    @router.post("/api/v1_0/tac-register/{tac_code}", response_model=api_models.TacRegisterPostModelResponse)
    async def request_post_with_id(tac_code: str, request_model:api_models.TacRegisterPostModelRequest, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('TacRegisterRouter.request_post_with_id start. tacCode:' + tac_code)
        auth_dict = BaseRouter.implementation_check(TacRegisterRouterConfig.is_post_with_id_available)
        response = api_models.TacRegisterPostModelResponse()
        auth_dict = BaseRouter.authorization_check(TacRegisterRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict)
                tac_code = session_context.check_context_code("TacCode", tac_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session,
                    session_context,
                    tac_code,
                    request_model
                )
            except TypeError as te:
                logging.info("TypeError Exception occurred")
                response.success = False
                traceback_string = "".join(traceback.format_tb(te.__traceback__))
                response.message = str(te) + " traceback:" + traceback_string
                logging.info("response.message:" + response.message)
            except Exception as e:
                logging.info("Exception occurred")
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
                logging.info("response.message:" + response.message)
            finally:
                if response.success == True:
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('TacRegisterRouter.submit get result:' + response.model_dump_json())
        return response

