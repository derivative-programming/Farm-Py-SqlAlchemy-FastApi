import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, AsyncMock
from  .....models import factory as request_factory
from apis import models as apis_models
from database import get_db
from helpers.api_token import ApiToken
import models.factory as model_factorys
from ..customer_user_log_out import CustomerUserLogOutRouterConfig
from main import app
import logging
import json
# from main import app

@pytest.mark.asyncio
async def test_init_success(overridden_get_db: AsyncSession, api_key_fixture:str):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True
@pytest.mark.asyncio
async def test_init_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': 'xxx'}
        )
        if CustomerUserLogOutRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': ''}
        )
        if CustomerUserLogOutRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(overridden_get_db: AsyncSession):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init'
        )
        if CustomerUserLogOutRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_endpoint_url_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_init_endpoint_invalid_code_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    customer_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_init_endpoint_method_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_submit_success(overridden_get_db, api_key_fixture:str):
    async def mock_process_request(session, session_context, customer_code, request):
            pass
    with patch.object(apis_models.CustomerUserLogOutPostModelResponse, 'process_request', new_callable=AsyncMock) as mock_method:
        mock_method.side_effect = mock_process_request
        customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
        customer_code = customer.code
        test_api_key = api_key_fixture
        async with AsyncClient(app=app, base_url="http://test") as ac:
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
async def test_submit_request_validation_error(overridden_get_db, api_key_fixture:str):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json=json.dumps({"xxxx":"yyyy"}),
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 400  # Expecting validation error for incorrect data
@pytest.mark.asyncio
async def test_submit_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json={},
            headers={'API_KEY': 'xxx'}
        )
        if CustomerUserLogOutRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json={},
            headers={'API_KEY': ''}
        )
        if CustomerUserLogOutRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_no_header(overridden_get_db: AsyncSession):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json={}
        )
        if CustomerUserLogOutRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}/xxxx',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_submit_endpoint_invalid_code_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    customer_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_submit_endpoint_method_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_code = customer.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/customer-user-log-out/{customer_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

def teardown_module(module):
    app.dependency_overrides.clear()
