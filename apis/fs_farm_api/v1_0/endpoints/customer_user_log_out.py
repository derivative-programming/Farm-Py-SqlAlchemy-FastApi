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
class CustomerUserLogOutRouterConfig():
    #constants
    is_get_available:bool = False
    is_get_with_id_available:bool = False
    is_get_init_available:bool = True
    is_get_to_csv_available:bool = False
    is_post_available:bool = False
    is_post_with_id_available:bool = True
    is_put_available:bool = False
    is_delete_available:bool = False
    is_public: bool = False
class CustomerUserLogOutRouter(BaseRouter):
    router = APIRouter()

    @staticmethod
    @router.get("/api/v1_0/customer-user-log-out/{customer_code}/init", response_model=api_init_models.CustomerUserLogOutInitObjWFGetInitModelResponse)
    async def request_get_init(customer_code: str, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('CustomerUserLogOutRouter.request_get_init start. customerCode:' + customer_code)
        auth_dict = BaseRouter.implementation_check(CustomerUserLogOutRouterConfig.is_get_init_available)
        response = api_init_models.CustomerUserLogOutInitObjWFGetInitModelResponse()
        auth_dict = BaseRouter.authorization_check(CustomerUserLogOutRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict)
                customer_code = session_context.check_context_code("CustomerCode", customer_code)
                init_request = api_init_models.CustomerUserLogOutInitObjWFGetInitModelRequest()
                response = await init_request.process_request(
                    session,
                    session_context,
                    customer_code,
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
        logging.info('CustomerUserLogOutRouter.init get result:' + response.model_dump_json())
        return response

    @staticmethod
    @router.post("/api/v1_0/customer-user-log-out/{customer_code}", response_model=api_models.CustomerUserLogOutPostModelResponse)
    async def request_post_with_id(customer_code: str, request_model:api_models.CustomerUserLogOutPostModelRequest, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('CustomerUserLogOutRouter.request_post_with_id start. customerCode:' + customer_code)
        auth_dict = BaseRouter.implementation_check(CustomerUserLogOutRouterConfig.is_post_with_id_available)
        response = api_models.CustomerUserLogOutPostModelResponse()
        auth_dict = BaseRouter.authorization_check(CustomerUserLogOutRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict)
                customer_code = session_context.check_context_code("CustomerCode", customer_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session,
                    session_context,
                    customer_code,
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
        logging.info('CustomerUserLogOutRouter.submit get result:' + response.model_dump_json())
        return response

