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
class CustomerBuildTempApiKeyRouterConfig():
    #constants
    isGetAvailable:bool = False
    isGetWithIdAvailable:bool = False
    isGetInitAvailable:bool = False
    isGetToCsvAvailable:bool = False
    isPostAvailable:bool = False
    isPostWithIdAvailable:bool = True
    isPutAvailable:bool = False
    isDeleteAvailable:bool = False
    isPublic: bool = False
class CustomerBuildTempApiKeyRouter(BaseRouter):
    router = APIRouter()

    @staticmethod
    @router.post("/api/v1_0/customer-build-temp-api-key/{customer_code}", response_model=api_models.CustomerBuildTempApiKeyPostModelResponse)
    async def request_post_with_id(customer_code: str, request_model:api_models.CustomerBuildTempApiKeyPostModelRequest, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('CustomerBuildTempApiKeyRouter.request_post_with_id start. customerCode:' + customer_code)
        auth_dict = BaseRouter.implementation_check(CustomerBuildTempApiKeyRouterConfig.isPostWithIdAvailable)
        # if CustomerBuildTempApiKeyRouterConfig.isPostWithIdAvailable == False:
        #     raise HTTPException(
        #         status_code=status.HTTP_501_NOT_IMPLEMENTED,
        #         detail="This method is not implemented.")
        response = api_models.CustomerBuildTempApiKeyPostModelResponse()
        auth_dict = BaseRouter.authorization_check(CustomerBuildTempApiKeyRouterConfig.isPublic, api_key)
        # auth_dict = dict()
        # if CustomerBuildTempApiKeyRouterConfig.isPublic == False:
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
        logging.info('CustomerBuildTempApiKeyRouter.submit get result:' + response.model_dump_json())
        return response

