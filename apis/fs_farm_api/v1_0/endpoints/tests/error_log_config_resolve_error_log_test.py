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
from ..error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogRouterConfig
from main import app
import logging
import json
# from main import app

@pytest.mark.asyncio
async def test_submit_success(overridden_get_db):
    async def mock_process_request(session, session_context, error_log_code, request):
            pass
    with patch.object(apis_models.ErrorLogConfigResolveErrorLogPostModelResponse, 'process_request', new_callable=AsyncMock) as mock_method:
        mock_method.side_effect = mock_process_request
        error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
        error_log_code = error_log.code
        api_dict = {'ErrorLogCode': str(error_log_code)}
        test_api_key = ApiToken.create_token(api_dict, 1)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.post(
                f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
                json={},
                headers={'API_KEY': test_api_key}
            )
            assert response.status_code == 200
            assert response.json()['success'] is False
            mock_method.assert_awaited()
@pytest.mark.asyncio
async def test_submit_request_validation_error(overridden_get_db):
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    api_dict = {'ErrorLogCode': str(error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json=json.dumps({"xxxx":"yyyy"}),
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 400  # Expecting validation error for incorrect data
@pytest.mark.asyncio
async def test_submit_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json={},
            headers={'API_KEY': 'xxx'}
        )
        if ErrorLogConfigResolveErrorLogRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json={},
            headers={'API_KEY': ''}
        )
        if ErrorLogConfigResolveErrorLogRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_no_header(overridden_get_db: AsyncSession):
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json={}
        )
        if ErrorLogConfigResolveErrorLogRouterConfig.is_public == True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(overridden_get_db: AsyncSession):
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    api_dict = {'ErrorLogCode': str(error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}/xxxx',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_submit_endpoint_invalid_code_failure(overridden_get_db: AsyncSession):
    error_log_code = uuid.UUID(int=0)
    api_dict = {'ErrorLogCode': str(error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_submit_endpoint_method_failure(overridden_get_db: AsyncSession):
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    api_dict = {'ErrorLogCode': str(error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

def teardown_module(module):
    app.dependency_overrides.clear()
