import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, AsyncMock
from .....models import factory as request_factory
from apis import models as apis_models
from database import get_db
from helpers.api_token import ApiToken
import models.factory as model_factorys
from ..plant_user_property_random_update import PlantUserPropertyRandomUpdateRouterConfig
from main import app
import logging
import json
# from main import app

@pytest.mark.asyncio
async def test_submit_success(overridden_get_db):
    async def mock_process_request(session, session_context, plant_code, request):
            pass
    with patch.object(apis_models.PlantUserPropertyRandomUpdatePostModelResponse, 'process_request', new_callable=AsyncMock) as mock_method:
        mock_method.side_effect = mock_process_request
        plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
        plant_code = plant.code
        api_dict = {'PlantCode': str(plant_code)}
        test_api_key = ApiToken.create_token(api_dict, 1)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.post(
                f'/api/v1_0/plant-user-property-random-update/{plant_code}',
                json={},
                headers={'API_KEY': test_api_key}
            )
            assert response.status_code == 200
            assert response.json()['success'] is False
            mock_method.assert_awaited()
@pytest.mark.asyncio
async def test_submit_request_validation_error(overridden_get_db):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
            json=json.dumps({"xxxx":"yyyy"}),
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 400  # Expecting validation error for incorrect data
@pytest.mark.asyncio
async def test_submit_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
            json={},
            headers={'API_KEY': 'xxx'}
        )
        if PlantUserPropertyRandomUpdateRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
            json={},
            headers={'API_KEY': ''}
        )
        if PlantUserPropertyRandomUpdateRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_no_header(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
            json={}
        )
        if PlantUserPropertyRandomUpdateRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}/xxxx',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_submit_endpoint_invalid_code_failure(overridden_get_db: AsyncSession):
    plant_code = uuid.UUID(int=0)
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_submit_endpoint_method_failure(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

def teardown_module(module):
    app.dependency_overrides.clear()
