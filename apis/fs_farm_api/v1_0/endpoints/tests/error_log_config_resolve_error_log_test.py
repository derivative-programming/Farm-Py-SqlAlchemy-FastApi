# apis/fs_farm_api/v1_0/endpoints/tests/error_log_config_resolve_error_log_test.py
"""
    #TODO add comment
"""
import logging
import uuid
import json  # pylint: disable=unused-import
from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import models.factory as model_factorys
from helpers.api_token import ApiToken  # pylint: disable=unused-import
from apis import models as apis_models
from database import get_db
from main import app
from .....models import factory as request_factory
from ..error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogRouterConfig

@pytest.mark.asyncio
async def test_submit_success(overridden_get_db):
    """
    #TODO add comment
    """
    async def mock_process_request(session, session_context, error_log_code, request):  # pylint: disable=unused-argument
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
    """
    #TODO add comment
    """
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    api_dict = {'ErrorLogCode': str(error_log_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json=json.dumps(
                {
                    "xxxx": "yyyy"
                }
            ),
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 400  # Expecting validation error for incorrect data
@pytest.mark.asyncio
async def test_submit_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    """
    #TODO add comment
    """
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json={},
            headers={'API_KEY': 'xxx'}
        )
        if ErrorLogConfigResolveErrorLogRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    """
    #TODO add comment
    """
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json={},
            headers={'API_KEY': ''}
        )
        if ErrorLogConfigResolveErrorLogRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_no_header(overridden_get_db: AsyncSession):
    """
    #TODO add comment
    """
    error_log = await model_factorys.ErrorLogFactory.create_async(overridden_get_db)
    error_log_code = error_log.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/error-log-config-resolve-error-log/{error_log_code}',
            json={}
        )
        if ErrorLogConfigResolveErrorLogRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(overridden_get_db: AsyncSession):
    """
    #TODO add comment
    """
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
    """
    #TODO add comment
    """
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
    """
    #TODO add comment
    """
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

def teardown_module(module):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    app.dependency_overrides.clear()
