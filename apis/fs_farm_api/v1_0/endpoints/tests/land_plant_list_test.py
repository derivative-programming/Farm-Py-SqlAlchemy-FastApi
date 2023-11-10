import json
import uuid
import pytest
from httpx import AsyncClient 
from sqlalchemy.ext.asyncio import AsyncSession
from  .....models import factory as request_factory
from database import get_db
from helpers.api_token import ApiToken
from models.factory.land import LandFactory  
from main import app
import logging
# from main import app
 
 
##GENTrainingBlock[caseisGetInitAvailable]Start
##GENLearn[isGetInitAvailable=true]Start 

@pytest.mark.asyncio
async def test_init_success(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
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
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init',
            headers={'API_KEY': 'xxx'}
            
        )
        assert response.status_code == 401 


@pytest.mark.asyncio
async def test_init_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init',
            headers={'API_KEY': ''}
            
        )
        assert response.status_code == 401 

@pytest.mark.asyncio
async def test_init_authorization_failure_no_header(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init' 
            
        )
        assert response.status_code == 401 

@pytest.mark.asyncio
async def test_init_endpoint_url_failure(overridden_get_db: AsyncSession): 
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501 
        
@pytest.mark.asyncio
async def test_init_endpoint_invalid_code_failure(overridden_get_db: AsyncSession):  
    land_code = uuid.UUID(int=0)
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200 
        assert response.json()['success'] is False


@pytest.mark.asyncio
async def test_init_endpoint_method_failure(overridden_get_db: AsyncSession): 
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
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
async def test_get_success(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    request = await request_factory.LandPlantListGetModelRequestFactory.create_async(overridden_get_db)
    logging.info("Test Request json...")
    logging.info(request.model_dump_json()) 
    logging.info("Test Request json dict...")
    logging.info(json.loads(request.model_dump_json())) 
    request_dict = request.to_dict_snake_serialized()
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
        assert response.json()['success'] is True


@pytest.mark.asyncio
async def test_get_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}',
            headers={'API_KEY': 'xxx'}
            
        )
        assert response.status_code == 401 


@pytest.mark.asyncio
async def test_get_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}',
            headers={'API_KEY': ''}
            
        )
        assert response.status_code == 401 

@pytest.mark.asyncio
async def test_get_authorization_failure_no_header(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}' 
            
        )
        assert response.status_code == 401 

@pytest.mark.asyncio
async def test_get_endpoint_url_failure(overridden_get_db: AsyncSession): 
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}/xxx',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501 
        
@pytest.mark.asyncio
async def test_get_endpoint_invalid_code_failure(overridden_get_db: AsyncSession):  
    land_code = uuid.UUID(int=0)
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-plant-list/{land_code}',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200 
        assert response.json()['success'] is False


@pytest.mark.asyncio
async def test_get_endpoint_method_failure(overridden_get_db: AsyncSession): 
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
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