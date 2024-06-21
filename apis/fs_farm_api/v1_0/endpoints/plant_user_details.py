# apis/fs_farm_api/v1_0/endpoints/plant_user_details.py
"""
This module contains the implementation of the
PlantUserDetailsRouter,
which handles the API endpoints related to the
Plant User Details.
The PlantUserDetailsRouter provides the following endpoints:
    - GET /api/v1_0/plant-user-details/{plant_code}/init:
        Get the initialization data for the
        Plant User Details page.
    - GET /api/v1_0/plant-user-details/{plant_code}:
        Get the Plant User Details Report
        for a specific plant code.
    - GET /api/v1_0/plant-user-details/{plant_code}/to-csv:
        Retrieve the Plant User Details
        Report as a CSV file.
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
PLANT_CODE = "Plant Code"
TRACEBACK = " traceback:"
EXCEPTION_OCCURRED = "Exception occurred: %s - %s"
class PlantUserDetailsRouterConfig():
    """
    Configuration class for the PlantUserDetailsRouter.
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
    Router class for the
    Plant User Details
    API endpoints.
    """
    router = APIRouter(tags=["PlantUserDetails"])

    @staticmethod
    @router.get(
        "/api/v1_0/plant-user-details/{plant_code}/init",
        response_model=(
            api_init_models.
            PlantUserDetailsInitReportGetInitModelResponse),
        summary="Plant User Details Init Page")
    async def request_get_init(
        plant_code: uuid.UUID = Path(..., description=PLANT_CODE),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the initialization data for the
        Plant User Details page.
        Args:
            plant_code (uuid.UUID): The UUID of the plant.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.
        Returns:
            PlantUserDetailsInitReportGetInitModelResponse:
                The initialization data for the
                Plant User Details page.
        """
        logging.info(
            'PlantUserDetailsRouter.request_get_init start. plantCode:%s',
            plant_code)
        auth_dict = BaseRouter.implementation_check(
            PlantUserDetailsRouterConfig.is_get_init_available)
        response = (
            api_init_models.
            PlantUserDetailsInitReportGetInitModelResponse()
        )
        auth_dict = BaseRouter.authorization_check(
            PlantUserDetailsRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                plant_code = session_context.check_context_code(
                    "PlantCode",
                    plant_code
                )
                init_request = (
                    api_init_models.
                    PlantUserDetailsInitReportGetInitModelRequest()
                )
                response = await init_request.process_request(
                    session_context,
                    plant_code,
                    response
                )
            except TypeError as te:
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(te.__traceback__))
                response.message = str(te) + TRACEBACK + traceback_string
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.info(
                    EXCEPTION_OCCURRED,
                    e.__class__.__name__,
                    e
                )
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__))
                response.message = str(e) + TRACEBACK + traceback_string
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
        plant_code: uuid.UUID = Path(..., description=PLANT_CODE),
        request_model: api_models.PlantUserDetailsGetModelRequest = Depends(),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the Plant User Details
        Report for a specific plant code.
        Args:
            plant_code (uuid.UUID): The unique identifier for the plant.
            request_model (api_models.PlantUserDetailsGetModelRequest):
                The request model for the API.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.
        Returns:
            api_models.PlantUserDetailsGetModelResponse: The response
                model containing the
                Plant User Details Report.
        Raises:
            Exception: If an error occurs during the processing of the request.
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
                logging.info('PlantUserDetailsRouter success')
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.info(
                    EXCEPTION_OCCURRED,
                    e.__class__.__name__,
                    e
                )
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__)
                )
                response.message = str(e) + TRACEBACK + traceback_string
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
        plant_code: uuid.UUID = Path(..., description=PLANT_CODE),
        request_model: api_models.PlantUserDetailsGetModelRequest = Depends(),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Retrieve the Plant User Details
        Report as a CSV file.
        Args:
            plant_code (uuid.UUID): The unique identifier for the plant.
            request_model (api_models.PlantUserDetailsGetModelRequest):
                The request model for the API.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.
        Returns:
            FileResponse: The CSV file containing the
            Plant User Details Report.
        """
        logging.info(
            "PlantUserDetailsRouter.request_get_with_id_to_csv"
            " start. plantCode:%s",
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
                report_items = [response_item.build_report_item() for
                                response_item in response.items]
                await report_manager.build_csv(tmp_file_path, report_items)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.info(
                    EXCEPTION_OCCURRED,
                    e.__class__.__name__,
                    e
                )
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__)
                )
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
        uuid_value = uuid.uuid4()
        output_file_name = (
            f'plant_user_details_{str(plant_code)}_{str(uuid_value)}.csv'
        )
        return FileResponse(
            tmp_file_path,
            media_type='text/csv',
            filename=output_file_name)

