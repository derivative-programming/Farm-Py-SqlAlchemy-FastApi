import tempfile
import uuid
from fastapi import APIRouter, Depends, Path
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
class PlantUserPropertyRandomUpdateRouterConfig():
    #constants
    is_get_available:bool = False
    is_get_with_id_available:bool = False
    is_get_init_available:bool = False
    is_get_to_csv_available:bool = False
    is_post_available:bool = False
    is_post_with_id_available:bool = True
    is_put_available:bool = False
    is_delete_available:bool = False
    is_public: bool = False
class PlantUserPropertyRandomUpdateRouter(BaseRouter):
    router = APIRouter(tags=["PlantUserPropertyRandomUpdate"])

    @staticmethod
    @router.post("/api/v1_0/plant-user-property-random-update/{plant_code}",
                 response_model=api_models.PlantUserPropertyRandomUpdatePostModelResponse,
                summary="Plant User Property Random Update Business Flow")
    async def request_post_with_id(plant_code: str,
                                   request_model:api_models.PlantUserPropertyRandomUpdatePostModelRequest,
                                   session:AsyncSession = Depends(get_db), api_key: str = Depends(api_key_header)):
        logging.info('PlantUserPropertyRandomUpdateRouter.request_post_with_id start. plantCode:' + plant_code)
        auth_dict = BaseRouter.implementation_check(PlantUserPropertyRandomUpdateRouterConfig.is_post_with_id_available)
        response = api_models.PlantUserPropertyRandomUpdatePostModelResponse()
        auth_dict = BaseRouter.authorization_check(PlantUserPropertyRandomUpdateRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                plant_code = session_context.check_context_code("PlantCode", plant_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    plant_code,
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
        logging.info('PlantUserPropertyRandomUpdateRouter.submit get result:' + response.model_dump_json())
        return response

