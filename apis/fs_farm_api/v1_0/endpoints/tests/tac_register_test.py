# apis/fs_farm_api/v1_0/endpoints/tests/tac_register_test.py
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
from ..tac_register import TacRegisterRouterConfig

@pytest.mark.asyncio
async def test_init_success(overridden_get_db: AsyncSession, api_key_fixture: str):
    """
    #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/tac-register/{tac_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True
@pytest.mark.asyncio
async def test_init_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    """
    #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/tac-register/{tac_code}/init',
            headers={'API_KEY': 'xxx'}
        )
        if TacRegisterRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    """
    #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/tac-register/{tac_code}/init',
            headers={'API_KEY': ''}
        )
        if TacRegisterRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(overridden_get_db: AsyncSession):
    """
    #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/tac-register/{tac_code}/init'
        )
        if TacRegisterRouterConfig.is_public is True:
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
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/tac-register/{tac_code}/init/xxx',
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
    tac_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/tac-register/{tac_code}/init',
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
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/tac-register/{tac_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_submit_success(overridden_get_db, api_key_fixture: str):
    """
        #TODO add comment
    """
    async def mock_process_request(session, session_context, tac_code, request):  # pylint: disable=unused-argument
        """
            #TODO add comment
        """
    with patch.object(
        apis_models.TacRegisterPostModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        tac = await model_factorys.TacFactory.create_async(overridden_get_db)
        tac_code = tac.code
        test_api_key = api_key_fixture
        async with AsyncClient(app=app, base_url="http://test") as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.post(
                f'/api/v1_0/tac-register/{tac_code}',
                json={},
                headers={'API_KEY': test_api_key}
            )
        assert response.status_code == 200
        assert response.json()['success'] is False
        mock_method.assert_awaited()
@pytest.mark.asyncio
async def test_submit_request_validation_error(overridden_get_db, api_key_fixture: str):
    """
        #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/tac-register/{tac_code}',
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
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/tac-register/{tac_code}',
            json={},
            headers={'API_KEY': 'xxx'}
        )
        if TacRegisterRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    """
        #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/tac-register/{tac_code}',
            json={},
            headers={'API_KEY': ''}
        )
        if TacRegisterRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_no_header(
    overridden_get_db: AsyncSession
):
    """
        #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/tac-register/{tac_code}',
            json={}
        )
        if TacRegisterRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(
    overridden_get_db: AsyncSession,
    api_key_fixture: str
):
    """
        #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/tac-register/{tac_code}/xxxx',
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
        #TODO add comment
    """
    tac_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/tac-register/{tac_code}',
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
        #TODO add comment
    """
    tac = await model_factorys.TacFactory.create_async(overridden_get_db)
    tac_code = tac.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/tac-register/{tac_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

def teardown_module(module):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    app.dependency_overrides.clear()
