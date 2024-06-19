# apis/fs_farm_api/v1_0/endpoints/tests/pac_user_tri_state_filter_list_test.py
# pylint: disable=unused-import
"""
    #TODO add comment
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
from ..pac_user_tri_state_filter_list import PacUserTriStateFilterListRouterConfig

@pytest.mark.asyncio
async def test_init_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True
@pytest.mark.asyncio
async def test_init_authorization_failure_bad_api_key(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/init',
            headers={'API_KEY': 'xxx'}
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/init',
            headers={'API_KEY': ''}
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/init'
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_endpoint_url_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/init/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_init_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    pac_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/init',
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
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    async def mock_process_request(
        session,
        session_context,
        pac_code,
        request
    ):  # pylint: disable=unused-argument
        pass
    with patch.object(
        apis_models.PacUserTriStateFilterListGetModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        pac = await model_factorys.PacFactory.create_async(overridden_get_db)
        pac_code = pac.code
        test_api_key = api_key_fixture
        request = await (
            request_factory.
            PacUserTriStateFilterListGetModelRequestFactory.
            create_async(
                overridden_get_db
            )
        )
        request_dict = request.to_dict_camel_serialized()
        logging.info("Test Request...")
        logging.info(request_dict)
        async with AsyncClient(
            app=app, base_url=test_constants.TEST_DOMAIN
        ) as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.get(
                f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}',
                params=request_dict,
                headers={'API_KEY': test_api_key}
            )
            assert response.status_code == 200
            assert response.json()['success'] is False
            mock_method.assert_awaited()
@pytest.mark.asyncio
async def test_get_authorization_failure_bad_api_key(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}',
            params=request_dict,
            headers={'API_KEY': 'xxx'}
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}',
            params=request_dict,
            headers={'API_KEY': ''}
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}',
            params=request_dict
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_endpoint_url_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/xxx',
            params=request_dict,
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_get_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    pac_code = uuid.UUID(int=0)
    request = await (
        request_factory.
        PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}',
            params=request_dict,
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_get_endpoint_method_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_csv_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    async def mock_process_request(
        session,
        session_context,
        pac_code,
        request
    ):  # pylint: disable=unused-argument
        pass
    with patch.object(
        apis_models.PacUserTriStateFilterListGetModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        pac = await model_factorys.PacFactory.create_async(overridden_get_db)
        pac_code = pac.code
        test_api_key = api_key_fixture
        request = await (
            request_factory.
            PacUserTriStateFilterListGetModelRequestFactory.
            create_async(
                overridden_get_db
            )
        )
        request_dict = request.to_dict_camel_serialized()
        logging.info("Test Request...")
        logging.info(request_dict)
        async with AsyncClient(
            app=app, base_url=test_constants.TEST_DOMAIN
        ) as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.get(
                f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv',
                params=request_dict,
                headers={'API_KEY': test_api_key}
            )
            assert response.status_code == 200
            assert response.headers['content-type'].startswith(
                test_constants.REPORT_TO_CSV_MEDIA_TYPE
            )
            mock_method.assert_awaited()
@pytest.mark.asyncio
async def test_get_csv_authorization_failure_bad_api_key(
    overridden_get_db: AsyncSession
):
    """
        #TODO add comment
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv',
            params=request_dict,
            headers={'API_KEY': 'xxx'}
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith(
                test_constants.REPORT_TO_CSV_MEDIA_TYPE
            )
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_csv_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    Test case to verify the behavior of the GET
    /api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv endpoint
    when the API key header is empty, and the user is not authorized.
    Steps:
    1. Create a test pac using the PacFactory.
    2. Create a PacUserTriStateFilterListGetModelRequest using the request_factory.
    3. Convert the request to a dictionary in camel case format.
    4. Send a GET request to the endpoint with the pac code
        and request parameters.
    5. Verify the response status code and content type based
        on the configuration.
    If the PacUserTriStateFilterListRouterConfig.is_public is True:
    - The response status code should be 200.
    - The response content type should start with the test_constants.
        REPORT_TO_CSV_MEDIA_TYPE.
    If the PacUserTriStateFilterListRouterConfig.is_public is False:
    - The response status code should be 401.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv',
            params=request_dict,
            headers={'API_KEY': ''}
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith(
                test_constants.REPORT_TO_CSV_MEDIA_TYPE
            )
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_csv_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
    Test case to check the behavior of the
    'get_csv_authorization_failure_no_header' endpoint.
    This test case verifies the response of the endpoint
    when the authorization header is missing.
    Steps:
    1. Create a test pac using the PacFactory.
    2. Create a test request using the
        PacUserTriStateFilterListGetModelRequestFactory.
    3. Send a GET request to the
        '/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv'
        endpoint with the request parameters.
    4. Verify the response status code and content type based
    on the configuration.
    If the 'is_public' flag in the PacUserTriStateFilterListRouterConfig is True:
    - The response status code should be 200.
    - The response content type should start with the
        'REPORT_TO_CSV_MEDIA_TYPE' defined in the test_constants.
    If the 'is_public' flag in the PacUserTriStateFilterListRouterConfig is False:
    - The response status code should be 401.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv',
            params=request_dict,
        )
        if PacUserTriStateFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith(
                test_constants.REPORT_TO_CSV_MEDIA_TYPE
            )
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_csv_endpoint_url_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for the failure scenario of the get_csv_endpoint_url function.
    This test case verifies that the API endpoint
        '/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv/xxx'
    returns a status code of 501 when an invalid API key is provided.
    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.
    Returns:
        None
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_get_csv_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for the 'get_csv_endpoint_invalid_code_failure' function.
    This test case verifies the behavior of the
        '/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv' endpoint
    when an invalid pac code is provided.
    Steps:
    1. Create a UUID representing an invalid pac code.
    2. Create a request object using the PacUserTriStateFilterListGetModelRequestFactory.
    3. Convert the request object to a dictionary
        in camel case serialization format.
    4. Set the test API key.
    5. Send a GET request to the
        '/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv'
        endpoint with the request parameters and headers.
    6. Assert that the response status code is 200.
    7. Assert that the response content type starts with the
        expected media type for CSV reports.
    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.
    Returns:
        None
    """
    pac_code = uuid.UUID(int=0)
    request = await (
        request_factory.
        PacUserTriStateFilterListGetModelRequestFactory.
        create_async(
            overridden_get_db
        )
    )
    request_dict = request.to_dict_camel_serialized()
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv',
            params=request_dict,
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.headers['content-type'].startswith(
            test_constants.REPORT_TO_CSV_MEDIA_TYPE
        )
@pytest.mark.asyncio
async def test_get_csv_endpoint_method_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for the failure scenario of the GET CSV endpoint method.
    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.
    Returns:
        None
    Raises:
        AssertionError: If the response status code is not 405.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv',
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
