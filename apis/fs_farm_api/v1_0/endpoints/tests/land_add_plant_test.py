# apis/fs_farm_api/v1_0/endpoints/tests/land_add_plant_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`land_add_plant` endpoint.
"""

import json
import uuid
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import models.factory as model_factorys
import pytest
from apis import models as apis_models
from apis.fs_farm_api.v1_0.endpoints.tests import test_constants
from database import get_db
from main import app

from ..land_add_plant import \
    LandAddPlantRouterConfig

# Test cases for the `submit` endpoint
##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=true,isGetInitAvailable=true]Start


@pytest.mark.asyncio
async def test_submit_success(overridden_get_db, api_key_fixture: str):
    """
    Test case for successful submission
    of a post to a land.

    Args:
        overridden_get_db (AsyncSession):
        The overridden database session.
        api_key_fixture (str): The API key fixture.

    Returns:
        None
    """
    async def mock_process_request(
        session,
        session_context,
        land_code,
        request
    ):  # pylint: disable=unused-argument
        """
        Mock function for processing the request.

        Args:
            session (AsyncSession): The database session.
            session_context: The session context.
            land_code: The land code.
            request: The request.

        Returns:
            None
        """

    with patch.object(
        apis_models.LandAddPlantPostModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:

        mock_method.side_effect = mock_process_request
        land = await \
            model_factorys.LandFactory.create_async(
                overridden_get_db)
        land_code = land.code
        test_api_key = api_key_fixture
        async with AsyncClient(
            app=app, base_url=test_constants.TEST_DOMAIN
        ) as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.post(
                "/api/v1_0/land-add-plant"
                f"/{land_code}",
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
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-add-plant"
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
    Test case for authorization failure with a bad API key.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-add-plant"
            f"/{land_code}",
            json={},
            headers={'API_KEY': 'xxx'}

        )

        if LandAddPlantRouterConfig.is_public is True:
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
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-add-plant"
            f"/{land_code}",
            json={},
            headers={'API_KEY': ''}

        )

        if LandAddPlantRouterConfig.is_public is True:
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
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-add-plant"
            f"/{land_code}",
            json={}

        )

        if LandAddPlantRouterConfig.is_public is True:
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
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-add-plant"
            f"/{land_code}/xxxx",
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
    land_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-add-plant"
            f"/{land_code}",
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
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/land-add-plant"
            f"/{land_code}",
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 405
##GENLearn[isPostWithIdAvailable=true,isGetInitAvailable=true]End
##GENTrainingBlock[caseisPostWithIdAvailable]End


# Test cases for the `init` endpoint
@pytest.mark.asyncio
async def test_init_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for successful initialization of the `land-add-plant` endpoint.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.

    Returns:
        None
    """
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/land-add-plant"
            f"/{land_code}/init",
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 200
        assert response.json()['success'] is True


@pytest.mark.asyncio
async def test_init_authorization_failure_bad_api_key(
    overridden_get_db: AsyncSession
):
    """
    Test case for authorization failure with a bad API key
    for the `init` endpoint.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/land-add-plant"
            f"/{land_code}/init",
            headers={'API_KEY': 'xxx'}

        )

        if LandAddPlantRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    Test case for authorization failure with an empty header
    key for the `init` endpoint.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/land-add-plant"
            f"/{land_code}/init",
            headers={'API_KEY': ''}

        )

        if LandAddPlantRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
    Test case to check authorization failure when no header is provided.

    This test case sends a GET request to the
    '/api/v1_0/land-add-plant/{land_code}/init' endpoint
    without providing the required authorization header.
    The expected behavior depends on the value
    of the 'is_public' flag in the
    LandAddPlantRouterConfig.
    If the flag is True, the response status
    code should be 200. Otherwise, the response status code should be 401.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.

    Returns:
        None
    """
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code

    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/land-add-plant"
            f"/{land_code}/init"
        )

        if LandAddPlantRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_endpoint_url_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for the failure scenario of the 'init'
    endpoint URL in the 'land-add-plant' API.

    This test verifies that when an invalid parameter is
    provided in the URL, the API returns a 501 status code.

    Args:
        overridden_get_db (AsyncSession): The overridden
            database session for testing.
        api_key_fixture (str): The API key for authentication.

    Returns:
        None
    """
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/land-add-plant"
            f"/{land_code}/init/xxx",
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 501


@pytest.mark.asyncio
async def test_init_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case to verify the behavior of the 'init' endpoint
    when an invalid land code is provided.

    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.
    """

    land_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            "/api/v1_0/land-add-plant"
            f"/{land_code}/init",
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
    Test case for the failure scenario of the `init` endpoint method.

    This test case verifies that when the `init` endpoint
    method is called with an invalid HTTP method,
    it returns a response with a status code of
    405 (Method Not Allowed).

    Args:
        overridden_get_db (AsyncSession): The overridden
            database session for testing.
        api_key_fixture (str): The API key fixture for testing.

    Returns:
        None
    """
    land = await \
        model_factorys.LandFactory.create_async(
            overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            "/api/v1_0/land-add-plant"
            f"/{land_code}/init",
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 405


def teardown_module():
    """
    Teardown function called after all tests in the module have been run.
    It clears the dependency overrides in the app.

    Args:
        module: The module object representing the test module.

    Returns:
        None
    """
    app.dependency_overrides.clear()
