# apis/fs_farm_api/v1_0/endpoints/pac_user_land_list.py
# pylint: disable=unused-import

"""
This module contains the implementation of the
PacUserLandListRouter,
which handles the API endpoints related to the
Pac User Land List.

The PacUserLandListRouter provides
the following endpoints:
- GET /api/v1_0/pac-user-land-list/...
    {pac_code}/init:
    Get the initialization data for the
    Pac User Land List page.
- GET /api/v1_0/pac-user-land-list/...
    {pac_code}:
    Get the Pac User Land List Report
    for a specific pac code.
- GET /api/v1_0/pac-user-land-list/...
        {pac_code}/to-csv:
    Retrieve the Pac User Land List
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

PAC_CODE = "Pac Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class PacUserLandListRouterConfig():
    """
    Configuration class for the
    PacUserLandListRouter.
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


class PacUserLandListRouter(BaseRouter):
    """
    Router class for the
    Pac User Land List
    API endpoints.
    """
    router = APIRouter(tags=["PacUserLandList"])


    @staticmethod
    @router.get(
        "/api/v1_0/pac-user-land-list"
        "/{pac_code}/init",
        response_model=(
            api_init_models.
            PacUserLandListInitReportGetInitModelResponse
        ),
        summary="Pac User Land List Init Page")
    async def request_get_init(
        pac_code: uuid.UUID = Path(..., description=PAC_CODE),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the initialization data for the
        Pac User Land List page.

        Args:
            pac_code (uuid.UUID): The UUID of the pac.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            PacUserLandListInitReportGetInitModelResponse:
                The initialization data for the
                Pac User Land List page.
        """

        logging.info(
            "PacUserLandListRouter"
            ".request_get_init start. pacCode:%s",
            pac_code)
        auth_dict = BaseRouter.implementation_check(
            PacUserLandListRouterConfig
            .is_get_init_available)

        response = (
            api_init_models.
            PacUserLandListInitReportGetInitModelResponse()
        )

        auth_dict = BaseRouter.authorization_check(
            PacUserLandListRouterConfig.is_public, api_key)

        init_request = (
            api_init_models.
            PacUserLandListInitReportGetInitModelRequest()
        )

        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                pac_code = session_context.check_context_code(
                    "PacCode",
                    pac_code
                )

                response = await init_request.process_request(
                    session_context,
                    pac_code,
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
            "PacUserLandListRouter"
            ".init get result:%s",
            response_data)
        return response


    @staticmethod
    @router.get(
        "/api/v1_0/pac-user-land-list"
        "/{pac_code}",
        response_model=(
            api_models
            .PacUserLandListGetModelResponse
        ),
        summary="Pac User Land List Report")
    async def request_get_with_id(
        pac_code: uuid.UUID = Path(..., description=PAC_CODE),
        request_model:
            api_models.PacUserLandListGetModelRequest = (
                Depends()),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the Pac User Land List
        Report for a specific pac code.

        Args:
            pac_code (uuid.UUID): The unique identifier for the pac.
            request_model (api_models.
            PacUserLandListGetModelRequest):
                The request model for the API.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            api_models.PacUserLandListGetModelResponse:
                The response
                model containing the
                Pac User Land List Report.

        Raises:
            Exception: If an error occurs during the processing of the request.
        """

        logging.info(
            "PacUserLandListRouter"
            ".request_get_with_id start. pacCode:%s",
            pac_code)
        auth_dict = BaseRouter.implementation_check(
            PacUserLandListRouterConfig
            .is_get_with_id_available)

        response = (api_models
                    .PacUserLandListGetModelResponse())

        auth_dict = BaseRouter.authorization_check(
            PacUserLandListRouterConfig.is_public, api_key)

        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict, session)
                pac_code = session_context.check_context_code(
                    "PacCode",
                    pac_code
                )
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    pac_code,
                    request_model
                )
                logging.info(
                    'PacUserLandListRouter success')
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
            "PacUserLandListRouter.submit get result:%s",
            response_data
        )
        return response


    @staticmethod
    @router.get(
        "/api/v1_0/pac-user-land-list"
        "/{pac_code}/to-csv",
        response_class=FileResponse,
        summary="Pac User Land List Report to CSV")
    async def request_get_with_id_to_csv(
        pac_code: uuid.UUID = Path(..., description=PAC_CODE),
        request_model:
            api_models.PacUserLandListGetModelRequest = (
                Depends()),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Retrieve the Pac User Land List
        Report as a CSV file.

        Args:
            pac_code (uuid.UUID): The unique identifier for the pac.
            request_model (api_models.
            PacUserLandListGetModelRequest):
                The request model for the API.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            FileResponse: The CSV file containing the
            Pac User Land List Report.
        """

        logging.info(
            "PacUserLandListRouter.request_get_with_id_to_csv"
            " start. pacCode:%s",
            pac_code
        )
        auth_dict = BaseRouter.implementation_check(
            PacUserLandListRouterConfig
            .is_get_to_csv_available)

        response = (api_models
                    .PacUserLandListGetModelResponse())

        auth_dict = BaseRouter.authorization_check(
            PacUserLandListRouterConfig
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
                pac_code = session_context.check_context_code(
                    "PacCode",
                    pac_code
                )
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    pac_code,
                    request_model
                )
                report_manager = \
                    reports.ReportManagerPacUserLandList(
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
            "PacUserLandListRouter"
            ".submit get result:%s",
            response_data
        )

        uuid_value = uuid.uuid4()

        output_file_name = (
            "pac_user_land_list_"
            f"{str(pac_code)}_{str(uuid_value)}.csv"
        )
        return FileResponse(
            tmp_file_path,
            media_type='text/csv',
            filename=output_file_name)
