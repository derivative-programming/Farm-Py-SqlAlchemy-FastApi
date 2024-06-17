# apis/fs_farm_api/v1_0/endpoints/tests/land_user_plant_multi_select_to_not_editable_test.py
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
from ..land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditableRouterConfig

@pytest.mark.asyncio
async def test_submit_success(overridden_get_db):
    """
    #TODO add comment
    """
    async def mock_process_request(
        session,
        session_context,
        land_code,
        request
    ):  # pylint: disable=unused-argument
        pass
    with patch.object(
        apis_models.LandUserPlantMultiSelectToNotEditablePostModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        land = await model_factorys.LandFactory.create_async(
            overridden_get_db
        )
        land_code = land.code
        api_dict = {'LandCode': str(land_code)}
        test_api_key = ApiToken.create_token(api_dict, 1)
        async with AsyncClient(
            app=app, base_url=test_constants.TEST_DOMAIN
        ) as ac:
            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.post(
                f'/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}',
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
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}',
            json=json.dumps(
                {
                    "xxxx": "yyyy"
                }
            ),
            headers={'API_KEY': test_api_key}
        )
        # Expecting validation error for incorrect data
        assert response.status_code == 400
@pytest.mark.asyncio
async def test_submit_authorization_failure_bad_api_key(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}',
            json={},
            headers={'API_KEY': 'xxx'}
        )
        if LandUserPlantMultiSelectToNotEditableRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}',
            json={},
            headers={'API_KEY': ''}
        )
        if LandUserPlantMultiSelectToNotEditableRouterConfig.is_public is True:
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
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}',
            json={}
        )
        if LandUserPlantMultiSelectToNotEditableRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401
@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}/xxxx',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501
@pytest.mark.asyncio
async def test_submit_endpoint_invalid_code_failure(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    land_code = uuid.UUID(int=0)
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False
@pytest.mark.asyncio
async def test_submit_endpoint_method_failure(
    overridden_get_db: AsyncSession
):
    """
    #TODO add comment
    """
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

def teardown_module(module):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    app.dependency_overrides.clear()
