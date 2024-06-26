# apis/fs_farm_api/v1_0/endpoints/tac_farm_dashboard.py
# pylint: disable=unused-import

"""
This module contains the implementation of the
TacFarmDashboardRouter,
which handles the API endpoints related to the
Tac Farm Dashboard.

The TacFarmDashboardRouter provides
the following endpoints:
- GET /api/v1_0/tac-farm-dashboard/...
    {tac_code}/init:
    Get the initialization data for the
    Tac Farm Dashboard page.
- GET /api/v1_0/tac-farm-dashboard/...
    {tac_code}:
    Get the Tac Farm Dashboard Report
    for a specific tac code.
- GET /api/v1_0/tac-farm-dashboard/...
        {tac_code}/to-csv:
    Retrieve the Tac Farm Dashboard
    Report as a CSV file.
"""

import logging
import tempfile  # noqa: F401
import traceback
import uuid

from fastapi import APIRouter, Depends, Path  # noqa: F401
from fastapi.responses import FileResponse  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession

import apis.models as api_models
import apis.models.init as api_init_models  # noqa: F401
import reports  # noqa: F401
from database import get_db
from helpers import SessionContext, api_key_header

from .base_router import BaseRouter

TAC_CODE = "Tac Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class TacFarmDashboardRouterConfig():
    """
    Configuration class for the
    TacFarmDashboardRouter.
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


class TacFarmDashboardRouter(BaseRouter):
    """
    Router class for the
    Tac Farm Dashboard
    API endpoints.
    """
    router = APIRouter(tags=["TacFarmDashboard"])


    @staticmethod
    @router.get(
        "/api/v1_0/tac-farm-dashboard"
        "/{tac_code}/init",
        response_model=(
            api_init_models.
            TacFarmDashboardInitReportGetInitModelResponse
        ),
        summary="Tac Farm Dashboard Init Page")
    async def request_get_init(
        tac_code: uuid.UUID = Path(..., description=TAC_CODE),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the initialization data for the
        Tac Farm Dashboard page.

        Args:
            tac_code (uuid.UUID): The UUID of the tac.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            TacFarmDashboardInitReportGetInitModelResponse:
                The initialization data for the
                Tac Farm Dashboard page.
        """

        logging.info(
            "TacFarmDashboardRouter"
            ".request_get_init start. tacCode:%s",
            tac_code)
        auth_dict = BaseRouter.implementation_check(
            TacFarmDashboardRouterConfig
            .is_get_init_available)

        response = (
            api_init_models.
            TacFarmDashboardInitReportGetInitModelResponse()
        )

        auth_dict = BaseRouter.authorization_check(
            TacFarmDashboardRouterConfig.is_public, api_key)

        init_request = (
            api_init_models.
            TacFarmDashboardInitReportGetInitModelRequest()
        )

        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                tac_code = session_context.check_context_code(
                    "TacCode",
                    tac_code
                )

                response = await init_request.process_request(
                    session_context,
                    tac_code,
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
        logging.info(
            "TacFarmDashboardRouter"
            ".init get result:%s",
            response_data)
        return response


    @staticmethod
    @router.get(
        "/api/v1_0/tac-farm-dashboard"
        "/{tac_code}",
        response_model=(
            api_models
            .TacFarmDashboardGetModelResponse
        ),
        summary="Tac Farm Dashboard Report")
    async def request_get_with_id(
        tac_code: uuid.UUID = Path(..., description=TAC_CODE),
        request_model:
            api_models.TacFarmDashboardGetModelRequest = (
                Depends()),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the Tac Farm Dashboard
        Report for a specific tac code.

        Args:
            tac_code (uuid.UUID): The unique identifier for the tac.
            request_model (api_models.
            TacFarmDashboardGetModelRequest):
                The request model for the API.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            api_models.TacFarmDashboardGetModelResponse:
                The response
                model containing the
                Tac Farm Dashboard Report.

        Raises:
            Exception: If an error occurs during the processing of the request.
        """

        logging.info(
            "TacFarmDashboardRouter"
            ".request_get_with_id start. tacCode:%s",
            tac_code)
        auth_dict = BaseRouter.implementation_check(
            TacFarmDashboardRouterConfig
            .is_get_with_id_available)

        response = (api_models
                    .TacFarmDashboardGetModelResponse())

        auth_dict = BaseRouter.authorization_check(
            TacFarmDashboardRouterConfig.is_public, api_key)

        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict, session)
                tac_code = session_context.check_context_code(
                    "TacCode",
                    tac_code
                )
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    tac_code,
                    request_model
                )
                logging.info(
                    'TacFarmDashboardRouter success')
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
            "TacFarmDashboardRouter.submit get result:%s",
            response_data
        )
        return response


    @staticmethod
    @router.get(
        "/api/v1_0/tac-farm-dashboard"
        "/{tac_code}/to-csv",
        response_class=FileResponse,
        summary="Tac Farm Dashboard Report to CSV")
    async def request_get_with_id_to_csv(
        tac_code: uuid.UUID = Path(..., description=TAC_CODE),
        request_model:
            api_models.TacFarmDashboardGetModelRequest = (
                Depends()),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Retrieve the Tac Farm Dashboard
        Report as a CSV file.

        Args:
            tac_code (uuid.UUID): The unique identifier for the tac.
            request_model (api_models.
            TacFarmDashboardGetModelRequest):
                The request model for the API.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            FileResponse: The CSV file containing the
            Tac Farm Dashboard Report.
        """

        logging.info(
            "TacFarmDashboardRouter.request_get_with_id_to_csv"
            " start. tacCode:%s",
            tac_code
        )
        auth_dict = BaseRouter.implementation_check(
            TacFarmDashboardRouterConfig
            .is_get_to_csv_available)

        response = (api_models
                    .TacFarmDashboardGetModelResponse())

        auth_dict = BaseRouter.authorization_check(
            TacFarmDashboardRouterConfig
            .is_public, api_key)

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
                tac_code = session_context.check_context_code(
                    "TacCode",
                    tac_code
                )
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    tac_code,
                    request_model
                )
                report_manager = \
                    reports.ReportManagerTacFarmDashboard(
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
            "TacFarmDashboardRouter"
            ".submit get result:%s",
            response_data
        )

        uuid_value = uuid.uuid4()

        output_file_name = (
            "tac_farm_dashboard_"
            f"{str(tac_code)}_{str(uuid_value)}.csv"
        )
        return FileResponse(
            tmp_file_path,
            media_type='text/csv',
            filename=output_file_name)
