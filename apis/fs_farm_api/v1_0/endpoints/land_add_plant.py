# apis/fs_farm_api/v1_0/endpoints/land_add_plant.py

"""
This module contains the implementation of the
LandAddPlantRouter class, which handles the
API endpoints related to adding plants to a land.
"""

import logging
import traceback
import uuid

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

import apis.models as api_models
import apis.models.init as api_init_models
from database import get_db
from helpers import SessionContext, api_key_header

from .base_router import BaseRouter

API_LOG_ERROR_FORMAT = "response.message: %s"


class LandAddPlantRouterConfig():
    """
    Configuration class for the LandAddPlantRouter.
    """

    # constants
    is_get_available: bool = False
    is_get_with_id_available: bool = False
    is_get_init_available: bool = True
    is_get_to_csv_available: bool = False
    is_post_available: bool = False
    is_post_with_id_available: bool = True
    is_put_available: bool = False
    is_delete_available: bool = False
    is_public: bool = False


class LandAddPlantRouter(BaseRouter):
    """
    Router class for the LandAddPlant API endpoints.
    """

    router = APIRouter(tags=["LandAddPlant"])

    @staticmethod
    @router.get(
        "/api/v1_0/land-add-plant/{land_code}/init",
        response_model=(
            api_init_models.LandAddPlantInitObjWFGetInitModelResponse
        ),
        summary="Land Add Plant Init Page"
    )
    async def request_get_init(
        land_code: uuid.UUID = Path(..., description="Land Code"),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Initialize the Land Add Plant process.

        Parameters:
        - land_code: The code of the land to add a plant.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with initialization details.
        """
        logging.info(
            'LandAddPlantRouter.request_get_init start. landCode:%s',
            land_code)
        auth_dict = BaseRouter.implementation_check(
            LandAddPlantRouterConfig.is_get_init_available)

        response = api_init_models.LandAddPlantInitObjWFGetInitModelResponse()

        auth_dict = BaseRouter.authorization_check(
            LandAddPlantRouterConfig.is_public, api_key)

        async with session:
            try:
                logging.info("Start session...")

                session_context = SessionContext(auth_dict, session)

                land_code = session_context.check_context_code(
                    "LandCode", land_code)

                init_request = (
                    api_init_models.LandAddPlantInitObjWFGetInitModelRequest()
                )
                response = await init_request.process_request(
                    session_context,
                    land_code,
                    response
                )
            except TypeError as te:
                logging.info("TypeError Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(te.__traceback__))
                response.message = f"{te} traceback: {traceback_string}"
                logging.info(API_LOG_ERROR_FORMAT, response.message)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.info("Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__)
                )
                response.message = f"{e} traceback: {traceback_string}"
                logging.info(API_LOG_ERROR_FORMAT, response.message)
            finally:
                if response.success is True:
                    await session.commit()
                else:
                    await session.rollback()
        response_data = response.model_dump_json()
        logging.info(
            'LandAddPlantRouter.init get result:%s',
            response_data)
        return response

##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=true]Start
    @staticmethod
    @router.post(
        "/api/v1_0/land-add-plant/{land_code}",
        response_model=api_models.LandAddPlantPostModelResponse,
        summary="Land Add Plant Business Flow")
    async def request_post_with_id(
        land_code: uuid.UUID,
        request_model: api_models.LandAddPlantPostModelRequest,
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Land Add Plant api post endpoint

        Parameters:
        - land_code: The code of the land object.
        - request_model: The request model containing
            the details of the item to be added.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with the result of the operation.
        """
        logging.info(
            "LandAddPlantRouter."
            "request_post_with_id start. landCode: %s",
            land_code
        )
        auth_dict = BaseRouter.implementation_check(
            LandAddPlantRouterConfig.is_post_with_id_available)

        response = api_models.LandAddPlantPostModelResponse()

        auth_dict = BaseRouter.authorization_check(
            LandAddPlantRouterConfig.is_public,
            api_key)

        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                land_code = session_context.check_context_code(
                    "LandCode",
                    land_code)

                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    land_code,
                    request_model
                )
            except TypeError as te:
                logging.info("TypeError Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(te.__traceback__)
                )
                response.message = f"{te} traceback: {traceback_string}"
                logging.info(API_LOG_ERROR_FORMAT, response.message)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.info("Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__)
                )
                response.message = f"{e} traceback: {traceback_string}"
                logging.info(API_LOG_ERROR_FORMAT, response.message)
            finally:
                if response.success is True:
                    await session.commit()
                else:
                    await session.rollback()
        response_data = response.model_dump_json()
        logging.info(
            'LandAddPlantRouter.submit get result:%s',
            response_data)
        return response
##GENLearn[isPostWithIdAvailable=true]End
##GENTrainingBlock[caseisPostWithIdAvailable]End
