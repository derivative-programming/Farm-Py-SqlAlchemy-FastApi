# apis/fs_farm_api/v1_0/endpoints/tests/plant_user_property_random_update_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the `plant_user_property_random_update` endpoint.
The `plant_user_property_random_update` endpoint is responsible for handling requests related to
the list of plants in a .
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
from ..plant_user_property_random_update import PlantUserPropertyRandomUpdateRouterConfig

@pytest.mark.asyncio
async def test_submit_success(overridden_get_db):
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
        apis_models.PlantUserPropertyRandomUpdatePostModelResponse,
        'process_request',
        new_callable=AsyncMock
    ) as mock_method:
        mock_method.side_effect = mock_process_request
        plant = await model_factorys.PlantFactory.create_async(
            overridden_get_db
        )
        plant_code = plant.code
        api_dict = {'PlantCode': str(plant_code)}
        test_api_key = ApiToken.create_token(api_dict, 1)
        async with AsyncClient(
            app=app, base_url=test_constants.TEST_DOMAIN
        ) as ac:
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
    """
    #TODO add comment
    """
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
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
async def test_submit_authorization_failure_empty_header_key(
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
async def test_submit_authorization_failure_no_header(
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
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
            json={}
        )
        if PlantUserPropertyRandomUpdateRouterConfig.is_public is True:
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}/xxxx',
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
    plant_code = uuid.UUID(int=0)
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
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
    plant = await model_factorys.PlantFactory.create_async(overridden_get_db)
    plant_code = plant.code
    api_dict = {'PlantCode': str(plant_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(
        app=app, base_url=test_constants.TEST_DOMAIN
    ) as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-property-random-update/{plant_code}',
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
