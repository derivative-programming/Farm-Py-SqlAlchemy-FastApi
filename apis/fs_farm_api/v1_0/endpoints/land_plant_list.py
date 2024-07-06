# apis/fs_farm_api/v1_0/endpoints/land_plant_list.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the implementation of the
LandPlantListRouter,
which handles the API endpoints related to the
Land Plant List.

The LandPlantListRouter provides
the following endpoints:
- GET /api/v1_0/land-plant-list/...
    {land_code}/init:
    Get the initialization data for the
    Land Plant List page.
- GET /api/v1_0/land-plant-list/...
    {land_code}:
    Get the Land Plant List Report
    for a specific land code.
- GET /api/v1_0/land-plant-list/...
        {land_code}/to-csv:
    Retrieve the Land Plant List
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

LAND_CODE = "Land Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class LandPlantListRouterConfig():  # pylint: disable=too-few-public-methods
    """
    Configuration class for the
    LandPlantListRouter.
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


class LandPlantListRouter(BaseRouter):
    """
    Router class for the
    Land Plant List
    API endpoints.
    """
    router = APIRouter(tags=["LandPlantList"])
##GENTrainingBlock[caseisGetInitAvailable]Start
##GENLearn[isGetInitAvailable=true]Start

    @staticmethod
    @router.get(
        "/api/v1_0/land-plant-list"
        "/{land_code}/init",
        response_model=(
            api_init_models.
            LandPlantListInitReportGetInitModelResponse
        ),
        summary="Land Plant List Init Page")
    async def request_get_init(
        land_code: uuid.UUID = Path(..., description=LAND_CODE),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the initialization data for the
        Land Plant List page.

        Args:
            land_code (uuid.UUID): The UUID of the land.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            LandPlantListInitReportGetInitModelResponse:
                The initialization data for the
                Land Plant List page.
        """

        logging.info(
            "LandPlantListRouter"
            ".request_get_init start. landCode:%s",
            land_code)
        auth_dict = BaseRouter.implementation_check(
            LandPlantListRouterConfig
            .is_get_init_available)

        response = (
            api_init_models.
            LandPlantListInitReportGetInitModelResponse()
        )

        auth_dict = BaseRouter.authorization_check(
            LandPlantListRouterConfig.is_public, api_key)

        init_request = (
            api_init_models.
            LandPlantListInitReportGetInitModelRequest()
        )

        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                land_code = session_context.check_context_code(
                    "LandCode",
                    land_code
                )

                response = await init_request.process_request(
                    session_context,
                    land_code,
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
            "LandPlantListRouter"
            ".init get result:%s",
            response_data)
        return response
##GENLearn[isGetInitAvailable=true]End
##GENTrainingBlock[caseisGetInitAvailable]End
##GENTrainingBlock[caseisGetAvailable]Start
##GENLearn[isGetAvailable=false]Start
##GENLearn[isGetAvailable=false]End
##GENTrainingBlock[caseisGetAvailable]End
##GENTrainingBlock[caseisGetWithIdAvailable]Start
##GENLearn[isGetWithIdAvailable=true]Start

    @staticmethod
    @router.get(
        "/api/v1_0/land-plant-list"
        "/{land_code}",
        response_model=(
            api_models
            .LandPlantListGetModelResponse
        ),
        summary="Land Plant List Report")
    async def request_get_with_id(
        land_code: uuid.UUID = Path(..., description=LAND_CODE),
        request_model:
            api_models.LandPlantListGetModelRequest = (
                Depends()),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the Land Plant List
        Report for a specific land code.

        Args:
            land_code (uuid.UUID): The unique identifier for the land.
            request_model (api_models.
            LandPlantListGetModelRequest):
                The request model for the API.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            api_models.LandPlantListGetModelResponse:
                The response
                model containing the
                Land Plant List Report.

        Raises:
            Exception: If an error occurs during the processing of the request.
        """

        logging.info(
            "LandPlantListRouter"
            ".request_get_with_id start. landCode:%s",
            land_code)
        auth_dict = BaseRouter.implementation_check(
            LandPlantListRouterConfig
            .is_get_with_id_available)

        response = (api_models
                    .LandPlantListGetModelResponse())

        auth_dict = BaseRouter.authorization_check(
            LandPlantListRouterConfig.is_public, api_key)

        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict, session)
                land_code = session_context.check_context_code(
                    "LandCode",
                    land_code
                )
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    land_code,
                    request_model
                )
                logging.info(
                    'LandPlantListRouter success')
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
            "LandPlantListRouter.submit get result:%s",
            response_data
        )
        return response
##GENLearn[isGetWithIdAvailable=true]End
##GENTrainingBlock[caseisGetWithIdAvailable]End
##GENTrainingBlock[caseisGetToCsvAvailable]Start
##GENLearn[isGetToCsvAvailable=true]Start

    @staticmethod
    @router.get(
        "/api/v1_0/land-plant-list"
        "/{land_code}/to-csv",
        response_class=FileResponse,
        summary="Land Plant List Report to CSV")
    async def request_get_with_id_to_csv(
        land_code: uuid.UUID = Path(..., description=LAND_CODE),
        request_model:
            api_models.LandPlantListGetModelRequest = (
                Depends()),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Retrieve the Land Plant List
        Report as a CSV file.

        Args:
            land_code (uuid.UUID): The unique identifier for the land.
            request_model (api_models.
            LandPlantListGetModelRequest):
                The request model for the API.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            FileResponse: The CSV file containing the
            Land Plant List Report.
        """

        logging.info(
            "LandPlantListRouter.request_get_with_id_to_csv"
            " start. landCode:%s",
            land_code
        )
        auth_dict = BaseRouter.implementation_check(
            LandPlantListRouterConfig
            .is_get_to_csv_available)

        response = (api_models
                    .LandPlantListGetModelResponse())

        auth_dict = BaseRouter.authorization_check(
            LandPlantListRouterConfig
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
                land_code = session_context.check_context_code(
                    "LandCode",
                    land_code
                )
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    land_code,
                    request_model
                )
                report_manager = \
                    reports.ReportManagerLandPlantList(
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
            "LandPlantListRouter"
            ".submit get result:%s",
            response_data
        )

        uuid_value = uuid.uuid4()

        output_file_name = (
            "land_plant_list_"
            f"{str(land_code)}_{str(uuid_value)}.csv"
        )
        return FileResponse(
            tmp_file_path,
            media_type='text/csv',
            filename=output_file_name)
##GENLearn[isGetToCsvAvailable=true]End
##GENTrainingBlock[caseisGetToCsvAvailable]End
##GENTrainingBlock[caseisPostAvailable]Start
##GENLearn[isPostAvailable=false]Start
##GENLearn[isPostAvailable=false]End
##GENTrainingBlock[caseisPostAvailable]End
##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=false]Start
##GENLearn[isPostWithIdAvailable=false]End
##GENTrainingBlock[caseisPostWithIdAvailable]End
##GENTrainingBlock[caseisPutAvailable]Start
##GENLearn[isPutAvailable=false]Start
##GENLearn[isPutAvailable=false]End
##GENTrainingBlock[caseisPutAvailable]End
##GENTrainingBlock[caseisDeleteAvailable]Start
##GENLearn[isDeleteAvailable=false]Start
##GENLearn[isDeleteAvailable=false]End
##GENTrainingBlock[caseisDeleteAvailable]End
