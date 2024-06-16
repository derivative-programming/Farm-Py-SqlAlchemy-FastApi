# apis/fs_farm_api/v1_0/endpoints/tests/plant_user_details_test.py
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
from .....models import factory as request_factory
from ..plant_user_details import PlantUserDetailsRouterConfig

@pytest.mark.asyncio
async def test_init_success(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
            headers={'API_KEY': 'xxx'}
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
            headers={'API_KEY': ''}
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init'
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init/xxx',
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
    plant_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
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
        plant_code,
        request
    ):  # pylint: disable=unused-argument
        pass
    with patch.object(
        apis_models.PlantUserDetailsGetModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
        plant_code = plant.code
        test_api_key = api_key_fixture
        request = await (
            request_factory.
            PlantUserDetailsGetModelRequestFactory.
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
                f'/api/v1_0/plant-user-details/{plant_code}',
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    request = await (
        request_factory.
        PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}',
            params=request_dict,
            headers={'API_KEY': 'xxx'}
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    request = await (
        request_factory.
        PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}',
            params=request_dict,
            headers={'API_KEY': ''}
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    request = await (
        request_factory.
        PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}',
            params=request_dict
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    request = await (
        request_factory.PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}/xxx',
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
    plant_code = uuid.UUID(int=0)
    request = await (
        request_factory.
        PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}',
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-details/{plant_code}',
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
        plant_code,
        request
    ):  # pylint: disable=unused-argument
        pass
    with patch.object(
        apis_models.PlantUserDetailsGetModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
        plant_code = plant.code
        test_api_key = api_key_fixture
        request = await (
            request_factory.
            PlantUserDetailsGetModelRequestFactory.
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
                f'/api/v1_0/plant-user-details/{plant_code}/to-csv',
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    request = await (
        request_factory.
        PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}/to-csv',
            params=request_dict,
            headers={'API_KEY': 'xxx'}
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
        #TODO add comment
    """
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    request = await (
        request_factory.
        PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}/to-csv',
            params=request_dict,
            headers={'API_KEY': ''}
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
        #TODO add comment
    """
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    request = await (
        request_factory.
        PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}/to-csv',
            params=request_dict,
        )
        if PlantUserDetailsRouterConfig.is_public is True:
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
    #TODO add comment
    """
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/to-csv/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_get_csv_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
    #TODO add comment
    """
    plant_code = uuid.UUID(int=0)
    request = await (
        request_factory.
        PlantUserDetailsGetModelRequestFactory.
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
            f'/api/v1_0/plant-user-details/{plant_code}/to-csv',
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
    #TODO add comment
    """
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    test_api_key = api_key_fixture
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-details/{plant_code}/to-csv',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

def teardown_module(module):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    app.dependency_overrides.clear()
