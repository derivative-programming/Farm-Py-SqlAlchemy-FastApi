from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
import traceback
import logging
from helpers import SessionContext, ApiToken, api_key_header
import apis.models.init as api_init_models
import apis.models as api_models
from database import get_db
class LandUserPlantMultiSelectToNotEditableRouterConfig():
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
class LandUserPlantMultiSelectToNotEditableRouter():
    router = APIRouter()

    @staticmethod
    @router.post("/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}", response_model=api_models.LandUserPlantMultiSelectToNotEditablePostModelResponse)
    async def request_post_with_id(land_code: str, request_model:api_models.LandUserPlantMultiSelectToNotEditablePostModelRequest, session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('LandUserPlantMultiSelectToNotEditableRouter.request_post_with_id start. landCode:' + land_code)
        if LandUserPlantMultiSelectToNotEditableRouterConfig.isPostWithIdAvailable == False:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="This method is not implemented.")
        response = api_models.LandUserPlantMultiSelectToNotEditablePostModelResponse()
        auth_dict = dict()
        if LandUserPlantMultiSelectToNotEditableRouterConfig.isPublic == False:
            auth_dict = ApiToken.validate_token(api_key)
            if auth_dict == None or len(auth_dict) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized.")
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
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
        logging.info('LandUserPlantMultiSelectToNotEditableRouter.submit get result:' + response.to_json())
        return response

