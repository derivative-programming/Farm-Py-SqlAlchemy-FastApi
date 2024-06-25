# apis/fs_farm_api/v1_0/endpoints/tests/customer_user_log_out_test.py
# pylint: disable=unused-import

"""
This module contains unit tests for the `customer_user_log_out` endpoint.
"""

import logging
import uuid
import json  # noqa: F401
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import apis.fs_farm_api.v1_0.endpoints.tests.test_constants as test_constants
import models.factory as model_factorys
from helpers.api_token import ApiToken  # noqa: F401
from apis import models as apis_models
from database import get_db
from main import app

from .....models import (  # pylint: disable=reimported
    factory as request_factory)
from ..customer_user_log_out import CustomerUserLogOutRouterConfig


@pytest.mark.asyncio
async def test_init_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test the successful initialization endpoint.
    """

    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True


@pytest.mark.asyncio
async def test_init_authorization_failure_bad_api_key(
    overridden_get_db: AsyncSession
):
    """
    Test the authorization failure with a bad API key during initialization.
    """

    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': 'xxx'}

        )
        if CustomerUserLogOutRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    Test the authorization failure with an
    empty header key during initialization.
    """

    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': ''}

        )
        if CustomerUserLogOutRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
    Test the authorization failure with no header during initialization.
    """

    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init'

        )
        if CustomerUserLogOutRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_endpoint_url_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test the failure of the endpoint URL during initialization.
    """

    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501


@pytest.mark.asyncio
async def test_init_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test the failure of the endpoint with an
    invalid customer code during initialization.
    """

    customer_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False


@pytest.mark.asyncio
async def test_init_endpoint_method_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test the failure of the endpoint with an
    invalid HTTP method during initialization.
    """

    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405


@pytest.mark.asyncio
async def test_submit_success(overridden_get_db, api_key_fixture: str):
    """
    Test case for successful submission of a post to a customer.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.

    Returns:
        None
    """
    async def mock_process_request(
        session,
        session_context,
        customer_code,
        request
    ):  # pylint: disable=unused-argument
        """
        Mock function for processing the request.

        Args:
            session (AsyncSession): The database session.
            session_context: The session context.
            customer_code: The customer code.
            request: The request.

        Returns:
            None
        """

    with patch.object(
        apis_models.CustomerUserLogOutPostModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:

        mock_method.side_effect = mock_process_request
        customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
        customer_code = customer.code
        test_api_key = api_key_fixture
        async with AsyncClient(
            app=app, base_url=test_constants.TEST_DOMAIN
        ) as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.post(
                f'/api/v1_0/customer-user-log-out/{customer_code}',
                json={},
                headers={'API_KEY': test_api_key}
            )

        assert response.status_code == 200
        assert response.json()['success'] is False
        mock_method.assert_awaited()


@pytest.mark.asyncio
async def test_submit_request_validation_error(
    overridden_get_db,
    api_key_fixture: str
):
    """
    Test case for submission of a post with validation error.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.

    Returns:
        None
    """
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
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
    Test case for authorization failure with a bad API key.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json={},
            headers={'API_KEY': 'xxx'}

        )

        if CustomerUserLogOutRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    Test case for authorization failure with an empty header key.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json={},
            headers={'API_KEY': ''}

        )

        if CustomerUserLogOutRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
    Test case for authorization failure with no header.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json={}

        )

        if CustomerUserLogOutRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for failure of the submit endpoint URL.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.

    Returns:
        None
    """
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}/xxxx',
            json={},
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 501


@pytest.mark.asyncio
async def test_submit_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for failure of the submit endpoint with an invalid code.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.

    Returns:
        None
    """
    customer_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json={},
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 200
        assert response.json()['success'] is False


@pytest.mark.asyncio
async def test_submit_endpoint_method_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for failure of the submit endpoint with an invalid method.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.

    Returns:
        None
    """
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
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

