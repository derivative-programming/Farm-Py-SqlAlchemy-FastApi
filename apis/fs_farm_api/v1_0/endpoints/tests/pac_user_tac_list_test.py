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
from ..pac_user_tac_list import PacUserTacListRouterConfig
from main import app
import logging
import json
# from main import app

@pytest.mark.asyncio
async def test_init_success(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True
@pytest.mark.asyncio
async def test_init_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/init',
            headers={'API_KEY': 'xxx'}
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/init',
            headers={'API_KEY': ''}
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/init'
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_endpoint_url_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/init/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_init_endpoint_invalid_code_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_init_endpoint_method_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_success(overridden_get_db: AsyncSession, api_key_fixture:str):
    async def mock_process_request(session, session_context, pac_code, request):
        pass
    with patch.object(apis_models.PacUserTacListGetModelResponse, 'process_request', new_callable=AsyncMock) as mock_method:
        mock_method.side_effect = mock_process_request
        pac = await model_factorys.PacFactory.create_async(overridden_get_db)
        pac_code = pac.code
        test_api_key = api_key_fixture
        request = await request_factory.PacUserTacListGetModelRequestFactory.create_async(overridden_get_db)
        request_dict = request.to_dict_camel_serialized()
        logging.info("Test Request...")
        logging.info(request_dict)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.get(
                f'/api/v1_0/pac-user-tac-list/{pac_code}',
                params=request_dict,
                headers={'API_KEY': test_api_key}
            )
            assert response.status_code == 200
            assert response.json()['success'] is False
            mock_method.assert_awaited()
@pytest.mark.asyncio
async def test_get_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}',
            headers={'API_KEY': 'xxx'}
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}',
            headers={'API_KEY': ''}
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_authorization_failure_no_header(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}'
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_endpoint_url_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_get_endpoint_invalid_code_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_get_endpoint_method_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/pac-user-tac-list/{pac_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_csv_success(overridden_get_db: AsyncSession, api_key_fixture:str):
    async def mock_process_request(session, session_context, pac_code, request):
        pass
    with patch.object(apis_models.PacUserTacListGetModelResponse, 'process_request', new_callable=AsyncMock) as mock_method:
        mock_method.side_effect = mock_process_request
        pac = await model_factorys.PacFactory.create_async(overridden_get_db)
        pac_code = pac.code
        test_api_key = api_key_fixture
        request = await request_factory.PacUserTacListGetModelRequestFactory.create_async(overridden_get_db)
        request_dict = request.to_dict_camel_serialized()
        logging.info("Test Request...")
        logging.info(request_dict)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.get(
                f'/api/v1_0/pac-user-tac-list/{pac_code}/to-csv',
                params=request_dict,
                headers={'API_KEY': test_api_key}
            )
            assert response.status_code == 200
            assert response.headers['content-type'].startswith('text/csv')
            mock_method.assert_awaited()
@pytest.mark.asyncio
async def test_get_csv_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/to-csv',
            headers={'API_KEY': 'xxx'}
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith('text/csv')
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_csv_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/to-csv',
            headers={'API_KEY': ''}
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith('text/csv')
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_csv_authorization_failure_no_header(overridden_get_db: AsyncSession):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/to-csv'
        )
        if PacUserTacListRouterConfig.is_public == True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith('text/csv')
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_csv_endpoint_url_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/to-csv/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_get_csv_endpoint_invalid_code_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/to-csv',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.headers['content-type'].startswith('text/csv')
@pytest.mark.asyncio
async def test_get_csv_endpoint_method_failure(overridden_get_db: AsyncSession, api_key_fixture:str):
    pac = await model_factorys.PacFactory.create_async(overridden_get_db)
    pac_code = pac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/pac-user-tac-list/{pac_code}/to-csv',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

def teardown_module(module):
    app.dependency_overrides.clear()
