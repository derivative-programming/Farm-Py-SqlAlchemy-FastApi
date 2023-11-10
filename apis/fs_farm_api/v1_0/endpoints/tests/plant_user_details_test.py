import json
import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from  .....models import factory as request_factory
from database import get_db
from helpers.api_token import ApiToken
import models.factory as model_factorys
from ..plant_user_details import PlantUserDetailsRouterConfig
from main import app
import logging
# from main import app

@pytest.mark.asyncio
async def test_init_success(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True
@pytest.mark.asyncio
async def test_init_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
            headers={'API_KEY': 'xxx'}
        )
        if PlantUserDetailsRouterConfig.isPublic == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
            headers={'API_KEY': ''}
        )
        if PlantUserDetailsRouterConfig.isPublic == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init'
        )
        if PlantUserDetailsRouterConfig.isPublic == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_endpoint_url_failure(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_init_endpoint_invalid_code_failure(overridden_get_db: AsyncSession):
    plant_code = uuid.UUID(int=0)
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_init_endpoint_method_failure(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-details/{plant_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_success(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    request = await request_factory.PlantUserDetailsGetModelRequestFactory.create_async(overridden_get_db)
    logging.info("Test Request json...")
    logging.info(request.model_dump_json())
    logging.info("Test Request json dict...")
    logging.info(json.loads(request.model_dump_json()))
    request_dict = request.to_dict_camel_serialized()
    logging.info("Test Request...")
    logging.info(request_dict)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}',
            params=request_dict,
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True
@pytest.mark.asyncio
async def test_get_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}',
            headers={'API_KEY': 'xxx'}
        )
        if PlantUserDetailsRouterConfig.isPublic == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}',
            headers={'API_KEY': ''}
        )
        if PlantUserDetailsRouterConfig.isPublic == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_authorization_failure_no_header(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}'
        )
        if PlantUserDetailsRouterConfig.isPublic == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_endpoint_url_failure(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_get_endpoint_invalid_code_failure(overridden_get_db: AsyncSession):
    plant_code = uuid.UUID(int=0)
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-details/{plant_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_get_endpoint_method_failure(overridden_get_db: AsyncSession):
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-details/{plant_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

def teardown_module(module):
    app.dependency_overrides.clear()