# apis/fs_farm_api/v1_0/endpoints/customer_build_temp_api_key.py
"""
    #TODO add comment
"""
import logging
import tempfile
import traceback
import uuid
from fastapi import APIRouter, Depends, Path
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import apis.models as api_models
import apis.models.init as api_init_models
import reports
from database import get_db
from helpers import SessionContext, api_key_header
from .base_router import BaseRouter
CUSTOMER_CODE = "Customer Code"
TRACEBACK = " traceback:"
EXCEPTION_OCCURRED = "Exception occurred: %s - %s"
class CustomerBuildTempApiKeyRouterConfig():
    """
        #TODO add comment
    """
    # constants
    is_get_available: bool = False
    is_get_with_id_available: bool = False
    is_get_init_available: bool = False
    is_get_to_csv_available: bool = False
    is_post_available: bool = False
    is_post_with_id_available: bool = True
    is_put_available: bool = False
    is_delete_available: bool = False
    is_public: bool = False
class CustomerBuildTempApiKeyRouter(BaseRouter):
    """
        #TODO add comment
    """
    router = APIRouter(tags=["CustomerBuildTempApiKey"])

    @staticmethod
    @router.post(
        "/api/v1_0/customer-build-temp-api-key/{customer_code}",
        response_model=api_models.CustomerBuildTempApiKeyPostModelResponse,
        summary="Customer Build Temp Api Key Business Flow")
    async def request_post_with_id(
        customer_code: uuid.UUID,
        request_model: api_models.CustomerBuildTempApiKeyPostModelRequest,
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
            #TODO add comment
        """
        logging.info(
            "CustomerBuildTempApiKeyRouter.request_post_with_id start. customerCode: %s",
            customer_code
        )
        auth_dict = BaseRouter.implementation_check(
            CustomerBuildTempApiKeyRouterConfig.is_post_with_id_available)
        response = api_models.CustomerBuildTempApiKeyPostModelResponse()
        auth_dict = BaseRouter.authorization_check(
            CustomerBuildTempApiKeyRouterConfig.is_public,
            api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                customer_code = session_context.check_context_code(
                    "CustomerCode",
                    customer_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    customer_code,
                    request_model
                )
            except TypeError as te:
                logging.info("TypeError Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(te.__traceback__)
                )
                response.message = str(te) + " traceback:" + traceback_string
                logging.info("response.message:%s", response.message)
            except Exception as e:
                logging.info("Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__)
                )
                response.message = str(e) + " traceback:" + traceback_string
                logging.info("response.message:%s", response.message)
            finally:
                if response.success is True:
                    await session.commit()
                else:
                    await session.rollback()
        response_data = response.model_dump_json()
        logging.info(
            'CustomerBuildTempApiKeyRouter.submit get result:%s',
            response_data)
        return response

