# apis/fs_farm_api/v1_0/endpoints/tests/error_log_config_resolve_error_log_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`error_log_config_resolve_error_log` endpoint.
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
from ..error_log_config_resolve_error_log import \
    ErrorLogConfigResolveErrorLogRouterConfig


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
        `ErrorLogConfigResolveErrorLogPostModelResponse`
        with the mock function.
    3. Create a error_log using the
        `ErrorLogFactory`.
    4. Generate an API key for the
        error_log.
    5. Send a POST request to the
        `error-log-config-resolve-error-log`
        endpoint with the error_log
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
        error_log_code,
        request
    ):  # pylint: disable=unused-argument
        pass

    with patch.object(
        apis_models.ErrorLogConfigResolveErrorLogPostModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        error_log = await model_factorys.ErrorLogFactory.create_async(
            overridden_get_db
        )
        error_log_code = error_log.code
        api_dict = {'ErrorLogCode': str(
            error_log_code)}
        test_api_key = ApiToken.create_token(api_dict, 1)
        async with AsyncClient(
            app=app, base_url=test_constants.TEST_DOMAIN
        ) as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.post(
                "/api/v1_0/error-log-config-resolve-error-log"
                f"/{error_log_code}",
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
    1. Create a error_log using the
        `ErrorLogFactory`.
    2. Generate an API key for the error_log.
    3. Send a POST request to the
        `error-log-config-resolve-error-log`
        endpoint with the error_log code,
        invalid data, and API key.
    4. Assert that the response status code is 400 (validation error).

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    error_log = await model_factorys.ErrorLogFactory.create_async(
        overridden_get_db)
    error_log_code = error_log.code
    api_dict = {'ErrorLogCode': str(
        error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/error-log-config-resolve-error-log"
            f"/{error_log_code}",
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
    1. Create a error_log using the
        ErrorLogFactory.
    2. Get the error_log code.
    3. Send a POST request to the
        '/api/v1_0/error-log-config-resolve-error-log/{error_log_code}'
        endpoint with an empty JSON payload and a bad API key.
    4. Verify the response status code based on the
        configuration of the ErrorLogConfigResolveErrorLogRouter.

    If the ErrorLogConfigResolveErrorLogRouterConfig.is_public is True,
    the expected response status code is 200.
    Otherwise, the expected response status code is 401.
    """
    error_log = await model_factorys.ErrorLogFactory.create_async(
        overridden_get_db)
    error_log_code = error_log.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/error-log-config-resolve-error-log"
            f"/{error_log_code}",
            json={},
            headers={'API_KEY': 'xxx'}
        )

        if ErrorLogConfigResolveErrorLogRouterConfig.is_public is True:
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
    '/api/v1_0/error-log-config-resolve-error-log/{error_log_code}'
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

    error_log = await model_factorys.ErrorLogFactory.create_async(
        overridden_get_db)
    error_log_code = error_log.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/error-log-config-resolve-error-log"
            f"/{error_log_code}",
            json={},
            headers={'API_KEY': ''}
        )

        if ErrorLogConfigResolveErrorLogRouterConfig.is_public is True:
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
    '/api/v1_0/error-log-config-resolve-error-log/{error_log_code}'
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
    error_log = await model_factorys.ErrorLogFactory.create_async(
        overridden_get_db)
    error_log_code = error_log.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/error-log-config-resolve-error-log"
            f"/{error_log_code}",
            json={}
        )

        if ErrorLogConfigResolveErrorLogRouterConfig.is_public is True:
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
    '/api/v1_0/error-log-config-resolve-error-log/{error_log_code}/xxxx'
    endpoint
    with an invalid URL parameter ('xxxx'). It verifies
    that the response status code is 501 (Not Implemented).

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    error_log = await model_factorys.ErrorLogFactory.create_async(
        overridden_get_db)
    error_log_code = error_log.code
    api_dict = {'ErrorLogCode': str(
        error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/error-log-config-resolve-error-log"
            f"/{error_log_code}/xxxx",
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
    error_log code is provided.
    This test case verifies that when an invalid
    error_log code is provided,
    the API returns a failure response with a status code of 200 and
    the 'success' field in the response JSON is set to False.
    """

    error_log_code = uuid.UUID(int=0)
    api_dict = {'ErrorLogCode': str(
        error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/error-log-config-resolve-error-log"
            f"/{error_log_code}",
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
    endpoint method when it fails to delete a error_log user.
    It creates a error_log using the
    ErrorLogFactory, generates
    an API token, and sends a GET request to the
    '/api/v1_0/error-log-config-resolve-error-log/{error_log_code}'
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
    error_log = await model_factorys.ErrorLogFactory.create_async(
        overridden_get_db)
    error_log_code = error_log.code
    api_dict = {'ErrorLogCode': str(
        error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/error-log-config-resolve-error-log"
            f"/{error_log_code}",
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 405


def teardown_module():
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
