# apis/fs_farm_api/v1_0/endpoints/tests/land_plant_list_test.py

"""
    #TODO add comment
"""

import uuid
import pytest
import logging
import json
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, AsyncMock
from .....models import factory as request_factory
from apis import models as apis_models
from database import get_db
from helpers.api_token import ApiToken
import models.factory as model_factorys
from ..land_plant_list import LandPlantListRouterConfig
from main import app
# from main import app


##GENTrainingBlock[caseisGetInitAvailable]Start
##GENLearn[isGetInitAvailable=true]Start

@pytest.mark.asyncio
async def test_init_success(overridden_get_db: AsyncSession, api_key_fixture: str):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True


@pytest.mark.asyncio
async def test_init_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init',
            headers={'API_KEY': 'xxx'}

        )
        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init',
            headers={'API_KEY': ''}

        )
        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init'

        )
        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_init_endpoint_url_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501


@pytest.mark.asyncio
async def test_init_endpoint_invalid_code_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is False


@pytest.mark.asyncio
async def test_init_endpoint_method_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-plant-list/{land_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405

##GENLearn[isGetInitAvailable=true]End
##GENTrainingBlock[caseisGetInitAvailable]End
##GENTrainingBlock[caseisGetAvailable]Start
##GENLearn[isGetAvailable=false]Start

##GENLearn[isGetAvailable=false]End
##GENTrainingBlock[caseisGetAvailable]End
##GENTrainingBlock[caseisGetWithIdAvailable]Start
##GENLearn[isGetWithIdAvailable=true]Start
@pytest.mark.asyncio
async def test_get_success(overridden_get_db: AsyncSession, api_key_fixture: str):
    async def mock_process_request(session, session_context, land_code, request):
        pass

    with patch.object(apis_models.LandPlantListGetModelResponse, 'process_request', new_callable=AsyncMock) as mock_method:
        mock_method.side_effect = mock_process_request

        land = await model_factorys.LandFactory.create_async(overridden_get_db)
        land_code = land.code
        test_api_key = api_key_fixture
        request = await request_factory.LandPlantListGetModelRequestFactory.create_async(overridden_get_db)
        request_dict = request.to_dict_camel_serialized()
        logging.info("Test Request...")
        logging.info(request_dict)
        async with AsyncClient(app=app, base_url="http://test") as ac:

            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.get(
                f'/api/v1_0/land-plant-list/{land_code}',
                params=request_dict,
                headers={'API_KEY': test_api_key}
            )

            assert response.status_code == 200
            assert response.json()['success'] is False
            mock_method.assert_awaited()


@pytest.mark.asyncio
async def test_get_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}',
            headers={'API_KEY': 'xxx'}

        )

        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}',
            headers={'API_KEY': ''}

        )

        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_authorization_failure_no_header(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}'

        )

        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_endpoint_url_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/xxx',
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 501


@pytest.mark.asyncio
async def test_get_endpoint_invalid_code_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}',
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 200
        assert response.json()['success'] is False


@pytest.mark.asyncio
async def test_get_endpoint_method_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-plant-list/{land_code}',
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 405
##GENLearn[isGetWithIdAvailable=true]End
##GENTrainingBlock[caseisGetWithIdAvailable]End
##GENTrainingBlock[caseisGetToCsvAvailable]Start
##GENLearn[isGetToCsvAvailable=true]Start


@pytest.mark.asyncio
async def test_get_csv_success(overridden_get_db: AsyncSession, api_key_fixture: str):
    async def mock_process_request(session, session_context, land_code, request):
        pass

    with patch.object(apis_models.LandPlantListGetModelResponse, 'process_request', new_callable=AsyncMock) as mock_method:
        mock_method.side_effect = mock_process_request

        land = await model_factorys.LandFactory.create_async(overridden_get_db)
        land_code = land.code
        test_api_key = api_key_fixture
        request = await request_factory.LandPlantListGetModelRequestFactory.create_async(overridden_get_db)
        request_dict = request.to_dict_camel_serialized()
        logging.info("Test Request...")
        logging.info(request_dict)
        async with AsyncClient(app=app, base_url="http://test") as ac:

            app.dependency_overrides[get_db] = lambda: overridden_get_db
            response = await ac.get(
                f'/api/v1_0/land-plant-list/{land_code}/to-csv',
                params=request_dict,
                headers={'API_KEY': test_api_key}
            )

            assert response.status_code == 200
            assert response.headers['content-type'].startswith('text/csv')
            mock_method.assert_awaited()


@pytest.mark.asyncio
async def test_get_csv_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/to-csv',
            headers={'API_KEY': 'xxx'}

        )

        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith('text/csv')
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_csv_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/to-csv',
            headers={'API_KEY': ''}

        )

        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith('text/csv')
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_csv_authorization_failure_no_header(overridden_get_db: AsyncSession):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/to-csv'

        )

        if LandPlantListRouterConfig.is_public is True:
            assert response.status_code == 200
            assert response.headers['content-type'].startswith('text/csv')
        else:
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_csv_endpoint_url_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/to-csv/xxx',
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 501


@pytest.mark.asyncio
async def test_get_csv_endpoint_invalid_code_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land_code = uuid.UUID(int=0)
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/to-csv',
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 200
        assert response.headers['content-type'].startswith('text/csv')


@pytest.mark.asyncio
async def test_get_csv_endpoint_method_failure(overridden_get_db: AsyncSession, api_key_fixture: str):
    land = await model_factorys.LandFactory.create_async(overridden_get_db)
    land_code = land.code
    test_api_key = api_key_fixture
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-plant-list/{land_code}/to-csv',
            headers={'API_KEY': test_api_key}
        )

        assert response.status_code == 405
##GENLearn[isGetToCsvAvailable=true]End
##GENTrainingBlock[caseisGetToCsvAvailable]End
##GENTrainingBlock[caseisPostAvailable]Start
##GENLearn[isPostAvailable=false]Start
##GENLearn[isPostAvailable=false]End
##GENTrainingBlock[caseisPostAvailable]End
##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=false]Start
##GENLearn[isPostWithIdAvailable=false]End
##GENTrainingBlock[caseisPostWithIdAvailable]End
##GENTrainingBlock[caseisPutAvailable]Start
##GENLearn[isPutAvailable=false]Start
##GENLearn[isPutAvailable=false]End
##GENTrainingBlock[caseisPutAvailable]End
##GENTrainingBlock[caseisDeleteAvailable]Start
##GENLearn[isDeleteAvailable=false]Start
##GENLearn[isDeleteAvailable=false]End
##GENTrainingBlock[caseisDeleteAvailable]End


def teardown_module(module):
    app.dependency_overrides.clear()
