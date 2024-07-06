# apis/fs_farm_api/v1_0/endpoints/tests/land_user_plant_multi_select_to_not_editable_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`land_user_plant_multi_select_to_not_editable` endpoint.
"""

import json  # noqa: F401
import logging  # noqa: F401
import uuid
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import models.factory as model_factorys  # noqa: F401
import pytest
from apis import models as apis_models
from apis.fs_farm_api.v1_0.endpoints.tests import test_constants
from database import get_db
from helpers.api_token import ApiToken  # noqa: F401
from main import app

from .....models import \
    factory as request_factory  # pylint: disable=reimported  # noqa: F401
from ..land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditableRouterConfig


@pytest.mark.asyncio
async def test_submit_success(overridden_get_db):
    """
    Test the successful submission of
    a delete request.

    This test ensures that a delete
    request is successfully
    processed and returns the expected response.

    Steps:
    1. Create a mock process_request function.
    2. Patch the `process_request` method of
        `LandUserPlantMultiSelectToNotEditablePostModelResponse`
        with the mock function.
    3. Create a land using the
        `LandFactory`.
    4. Generate an API key for the
        land.
    5. Send a POST request to the
        `land-user-plant-multi-select-to-not-editable`
        endpoint with the land
        code and API key.
    6. Assert that the response status code is 200 and
        the 'success' field in the response JSON is False.
    7. Assert that the `process_request` method was called.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    async def mock_process_request(
        session,
        session_context,
        land_code,
        request
    ):  # pylint: disable=unused-argument
        pass

    with patch.object(
        apis_models.LandUserPlantMultiSelectToNotEditablePostModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        land = await model_factorys.LandFactory.create_async(
            overridden_get_db
        )
        land_code = land.code
        api_dict = {'LandCode': str(
            land_code)}
        test_api_key = ApiToken.create_token(api_dict, 1)
        async with AsyncClient(
            app=app, base_url=test_constants.TEST_DOMAIN
        ) as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.post(
                "/api/v1_0/land-user-plant-multi-select-to-not-editable"
                f"/{land_code}",
                json={},
                headers={'API_KEY': test_api_key}
            )

            assert response.status_code == 200
            assert response.json()['success'] is False
            mock_method.assert_awaited()


@pytest.mark.asyncio
async def test_submit_request_validation_error(overridden_get_db):
    """
    Test the submission of a delete request with
    validation errors.

    This test ensures that a delete request with
    incorrect data results in a validation error.

    Steps:
    1. Create a land using the
        `LandFactory`.
    2. Generate an API key for the land.
    3. Send a POST request to the
        `land-user-plant-multi-select-to-not-editable`
        endpoint with the land code,
        invalid data, and API key.
    4. Assert that the response status code is 400 (validation error).

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    land = await model_factorys.LandFactory.create_async(
        overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(
        land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-user-plant-multi-select-to-not-editable"
            f"/{land_code}",
            json=json.dumps(
                {
                    "xxxx": "yyyy"
                }
            ),
            headers={'API_KEY': test_api_key}
        )
        # Expecting validation error for incorrect data
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_submit_authorization_failure_bad_api_key(
    overridden_get_db: AsyncSession
):
    """
    Test case to verify the behavior when submitting a
    request with a bad API key for authorization failure.

    Steps:
    1. Create a land using the
        LandFactory.
    2. Get the land code.
    3. Send a POST request to the
        '/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}'
        endpoint with an empty JSON payload and a bad API key.
    4. Verify the response status code based on the
        configuration of the LandUserPlantMultiSelectToNotEditableRouter.

    If the LandUserPlantMultiSelectToNotEditableRouterConfig.is_public is True,
    the expected response status code is 200.
    Otherwise, the expected response status code is 401.
    """
    land = await model_factorys.LandFactory.create_async(
        overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-user-plant-multi-select-to-not-editable"
            f"/{land_code}",
            json={},
            headers={'API_KEY': 'xxx'}
        )

        if LandUserPlantMultiSelectToNotEditableRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    Test case to verify the behavior when submitting a
    request without header.

    This test case sends a POST request to the
    '/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}'
    endpoint
    without providing an authorization header.
    It checks whether the response status code is 401
    if the endpoint is not public, or 200 if
    the endpoint is public.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """

    land = await model_factorys.LandFactory.create_async(
        overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-user-plant-multi-select-to-not-editable"
            f"/{land_code}",
            json={},
            headers={'API_KEY': ''}
        )

        if LandUserPlantMultiSelectToNotEditableRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
    Test case to verify the behavior when submitting a
    request without authorization header.

    This test case sends a POST request to the
    '/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}'
    endpoint
    without providing an authorization header.
    It checks whether the response status code is 401
    if the endpoint is not public, or 200 if the
    endpoint is public.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    land = await model_factorys.LandFactory.create_async(
        overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-user-plant-multi-select-to-not-editable"
            f"/{land_code}",
            json={}
        )

        if LandUserPlantMultiSelectToNotEditableRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(
    overridden_get_db: AsyncSession
):
    """
    Test the failure of the submit endpoint URL.

    This test case sends a POST request to the
    '/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}/xxxx'
    endpoint
    with an invalid URL parameter ('xxxx'). It verifies
    that the response status code is 501 (Not Implemented).

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    land = await model_factorys.LandFactory.create_async(
        overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(
        land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-user-plant-multi-select-to-not-editable"
            f"/{land_code}/xxxx",
            json={},
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 501


@pytest.mark.asyncio
async def test_submit_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession
):
    """
    Test case for the submit endpoint when an invalid
    land code is provided.
    This test case verifies that when an invalid
    land code is provided,
    the API returns a failure response with a status code of 200 and
    the 'success' field in the response JSON is set to False.
    """

    land_code = uuid.UUID(int=0)
    api_dict = {'LandCode': str(
        land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-user-plant-multi-select-to-not-editable"
            f"/{land_code}",
            json={},
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 200
        assert response.json()['success'] is False


@pytest.mark.asyncio
async def test_submit_endpoint_method_failure(
    overridden_get_db: AsyncSession
):
    """
    Test the failure of the submit endpoint method.

    This test case checks the behavior of the submit
    endpoint method when it fails to delete a land user.
    It creates a land using the
    LandFactory, generates
    an API token, and sends a GET request to the
    '/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}'
    endpoint
    with the API key in the headers. The expected
    response status code is 405 (Method Not Allowed).

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 405.

    """
    land = await model_factorys.LandFactory.create_async(
        overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(
        land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/land-user-plant-multi-select-to-not-editable"
            f"/{land_code}",
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 405


def teardown_module(module):  # pylint: disable=unused-argument
    """
    Teardown function for the module.

    This function is called after all the tests
    in the module have been executed.
    It clears the dependency overrides for the app.

    Args:
        module: The module object.

    Returns:
        None
    """
    app.dependency_overrides.clear()
