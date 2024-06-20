# apis/fs_farm_api/v1_0/endpoints/tests/pac_user_date_greater_than_filter_list_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the `pac_user_date_greater_than_filter_list` endpoint.
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
from ..pac_user_date_greater_than_filter_list import PacUserDateGreaterThanFilterListRouterConfig

@pytest.mark.asyncio
async def test_init_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test the successful initialization endpoint.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/init',
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
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/init',
            headers={'API_KEY': 'xxx'}
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
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
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/init',
            headers={'API_KEY': ''}
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
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
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/init'
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
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
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/init/xxx',
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
    invalid pac code during initialization.
    """
    pac_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/init',
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
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test the successful retrieval of the `pac_user_date_greater_than_filter_list` get endpoint.
    """
    async def mock_process_request(
        session,
        session_context,
        pac_code,
        request
    ):  # pylint: disable=unused-argument
        pass
    with patch.object(
        apis_models.PacUserDateGreaterThanFilterListGetModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        pac = await model_factorys.PacFactory.create_async(overridden_get_db)
        pac_code = pac.code
        test_api_key = api_key_fixture
        request = await (
            request_factory.
            PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
                f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}',
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
    Test the authorization failure with a bad API key during retrieval.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}',
            params=request_dict,
            headers={'API_KEY': 'xxx'}
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    Test the authorization failure with an empty header key during retrieval.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}',
            params=request_dict,
            headers={'API_KEY': ''}
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
    Test case to verify authorization failure when no header is provided.
    This test case sends a GET request to the
    '/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}' endpoint
    without providing the required authorization
    header. It checks whether the response status code
    is 401 (Unauthorized) if the endpoint is not
    public, or 200 (OK) if the endpoint is public.
    Args:
        overridden_get_db (AsyncSession): The overridden database session.
    Returns:
        None
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}',
            params=request_dict
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_endpoint_url_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for the failure scenario of the GET endpoint URL.
    This test case verifies that the API returns the expected
    response when an invalid URL is provided.
    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.
    Returns:
        None
    Raises:
        AssertionError: If the response status code is not 501.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/xxx',
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
    Test case for the GET endpoint when an invalid pac code is provided.
    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.
    Returns:
        None
    """
    pac_code = uuid.UUID(int=0)
    request = await (
        request_factory.
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}',
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
    Test case for the failure scenario of the GET endpoint method.
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
        response = await ac.post(
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_csv_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    Test case for successful retrieval of CSV data.
    Args:
        overridden_get_db (AsyncSession): The overridden database session.
        api_key_fixture (str): The API key fixture.
    Returns:
        None
    """
    async def mock_process_request(
        session,
        session_context,
        pac_code,
        request
    ):  # pylint: disable=unused-argument
        pass
    with patch.object(
        apis_models.PacUserDateGreaterThanFilterListGetModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        pac = await model_factorys.PacFactory.create_async(overridden_get_db)
        pac_code = pac.code
        test_api_key = api_key_fixture
        request = await (
            request_factory.
            PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
                f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv',
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
    Test case to verify the behavior of the API
    when an invalid API key is provided.
    This test case sends a GET request to the
    '/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv' endpoint
    with an invalid API key in the headers.
    The expected behavior is a 401 Unauthorized response.
    Steps:
    1. Create a test pac using the PacFactory.
    2. Create a PacUserDateGreaterThanFilterListGetModelRequest using
        the PacUserDateGreaterThanFilterListGetModelRequestFactory.
    3. Convert the request object to a dictionary.
    4. Send a GET request to the API endpoint with
        the pac code and request parameters.
    5. Assert that the response status code is 401
        if the endpoint is not public.
       Otherwise, assert that the response status code
        is 200 and the content-type header
       starts with the expected media type for CSV reports.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv',
            params=request_dict,
            headers={'API_KEY': 'xxx'}
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
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
    /api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv endpoint
    when the API key header is empty, and the user is not authorized.
    Steps:
    1. Create a test pac using the PacFactory.
    2. Create a PacUserDateGreaterThanFilterListGetModelRequest using the request_factory.
    3. Convert the request to a dictionary in camel case format.
    4. Send a GET request to the endpoint with the pac code
        and request parameters.
    5. Verify the response status code and content type based
        on the configuration.
    If the PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
    - The response status code should be 200.
    - The response content type should start with the test_constants.
        REPORT_TO_CSV_MEDIA_TYPE.
    If the PacUserDateGreaterThanFilterListRouterConfig.is_public is False:
    - The response status code should be 401.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv',
            params=request_dict,
            headers={'API_KEY': ''}
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
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
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
    3. Send a GET request to the
        '/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv'
        endpoint with the request parameters.
    4. Verify the response status code and content type based
    on the configuration.
    If the 'is_public' flag in the PacUserDateGreaterThanFilterListRouterConfig is True:
    - The response status code should be 200.
    - The response content type should start with the
        'REPORT_TO_CSV_MEDIA_TYPE' defined in the test_constants.
    If the 'is_public' flag in the PacUserDateGreaterThanFilterListRouterConfig is False:
    - The response status code should be 401.
    """
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    request = await (
        request_factory.
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv',
            params=request_dict,
        )
        if PacUserDateGreaterThanFilterListRouterConfig.is_public is True:
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
        '/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv/xxx'
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv/xxx',
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
        '/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv' endpoint
    when an invalid pac code is provided.
    Steps:
    1. Create a UUID representing an invalid pac code.
    2. Create a request object using the PacUserDateGreaterThanFilterListGetModelRequestFactory.
    3. Convert the request object to a dictionary
        in camel case serialization format.
    4. Set the test API key.
    5. Send a GET request to the
        '/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv'
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
        PacUserDateGreaterThanFilterListGetModelRequestFactory.
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv',
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
            f'/api/v1_0/pac-user-date-greater-than-filter-list/{pac_code}/to-csv',
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
