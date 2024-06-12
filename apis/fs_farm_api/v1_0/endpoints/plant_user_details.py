# apis/fs_farm_api/v1_0/endpoints/plant_user_details.py
"""
    #TODO add comment
"""
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
from .base_router import BaseRouter
from database import get_db
class PlantUserDetailsRouterConfig():
    """
        #TODO add comment
    """
    # constants
    is_get_available: bool = False
    is_get_with_id_available: bool = True
    is_get_init_available: bool = True
    is_get_to_csv_available: bool = True
    is_post_available: bool = False
    is_post_with_id_available: bool = False
    is_put_available: bool = False
    is_delete_available: bool = False
    is_public: bool = False
class PlantUserDetailsRouter(BaseRouter):
    """
        #TODO add comment
    """
    router = APIRouter(tags=["PlantUserDetails"])

    @staticmethod
    @router.get(
        "/api/v1_0/plant-user-details/{plant_code}/init",
        response_model=api_init_models.PlantUserDetailsInitReportGetInitModelResponse,
        summary="Plant User Details Init Page")
    async def request_get_init(
        plant_code: str = Path(..., description="Plant Code"),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
            #TODO add comment
        """
        logging.info(
            'PlantUserDetailsRouter.request_get_init start. plantCode:%s',
            plant_code)
        auth_dict = BaseRouter.implementation_check(
            PlantUserDetailsRouterConfig.is_get_init_available)
        response = api_init_models.PlantUserDetailsInitReportGetInitModelResponse()
        auth_dict = BaseRouter.authorization_check(
            PlantUserDetailsRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                plant_code = session_context.check_context_code(
                    "PlantCode",
                    plant_code)
                init_request = api_init_models.PlantUserDetailsInitReportGetInitModelRequest()
                response = await init_request.process_request(
                    session_context,
                    plant_code,
                    response
                )
            except TypeError as te:
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(te.__traceback__))
                response.message = str(te) + " traceback:" + traceback_string
            except Exception as e:
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success is True:
                    await session.commit()
                else:
                    await session.rollback()
        response_data = response.model_dump_json()
        logging.info('PlantUserDetailsRouter.init get result:%s',
                     response_data)
        return response

    @staticmethod
    @router.get(
        "/api/v1_0/plant-user-details/{plant_code}",
        response_model=api_models.PlantUserDetailsGetModelResponse,
        summary="Plant User Details Report")
    async def request_get_with_id(
        plant_code: str = Path(..., description="Plant Code"),
        request_model: api_models.PlantUserDetailsGetModelRequest = Depends(),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
            #TODO add comment
        """
        logging.info(
            'PlantUserDetailsRouter.request_get_with_id start. plantCode:%s',
            plant_code)
        auth_dict = BaseRouter.implementation_check(
            PlantUserDetailsRouterConfig.is_get_with_id_available)
        response = api_models.PlantUserDetailsGetModelResponse()
        auth_dict = BaseRouter.authorization_check(
            PlantUserDetailsRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict, session)
                plant_code = session_context.check_context_code(
                    "PlantCode",
                    plant_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
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
                if response.success is True:
                    await session.commit()
                else:
                    await session.rollback()
        response_data = response.model_dump_json()
        logging.info(
            "PlantUserDetailsRouter.submit get result:%s",
            response_data
        )
        return response

    @staticmethod
    @router.get(
        "/api/v1_0/plant-user-details/{plant_code}/to-csv",
        response_class=FileResponse,
        summary="Plant User Details Report to CSV")
    async def request_get_with_id_to_csv(
        plant_code: str = Path(..., description="Plant Code"),
        request_model: api_models.PlantUserDetailsGetModelRequest = Depends(),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        logging.info(
            "PlantUserDetailsRouter.request_get_with_id_to_csv start. plantCode:%s",
                plant_code
        )
        auth_dict = BaseRouter.implementation_check(
            PlantUserDetailsRouterConfig.is_get_to_csv_available)
        response = api_models.PlantUserDetailsGetModelResponse()
        auth_dict = BaseRouter.authorization_check(
            PlantUserDetailsRouterConfig.is_public, api_key)
        tmp_file_path = ""
        with tempfile.NamedTemporaryFile(
            delete=False,
            mode='w',
            suffix='.csv',
            encoding='utf-8'
        ) as tmp_file:
            tmp_file_path = tmp_file.name
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict, session)
                plant_code = session_context.check_context_code(
                    "PlantCode",
                    plant_code
                )
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    plant_code,
                    request_model
                )
                report_manager = reports.ReportManagerPlantUserDetails(
                    session_context)
                report_manager.build_csv(tmp_file_path, response.items)
            except Exception as e:
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success is True:
                    await session.commit()
                else:
                    await session.rollback()
        response_data = response.model_dump_json()
        logging.info(
            'PlantUserDetailsRouter.submit get result:%s', response_data
        )
        output_file_name = 'plant_user_details_' + plant_code + '_' + str(uuid.uuid4()) + '.csv'
        return FileResponse(
            tmp_file_path,
            media_type='text/csv',
            filename=output_file_name)

