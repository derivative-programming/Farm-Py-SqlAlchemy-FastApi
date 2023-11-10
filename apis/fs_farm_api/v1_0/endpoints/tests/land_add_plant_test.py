import json
import uuid
import pytest
from httpx import AsyncClient 
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from helpers.api_token import ApiToken
from models.factory.land import LandFactory 
from .....models.factory.land_add_plant  import LandAddPlantPostModelRequestFactory 
from main import app
# from main import app
    

##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=true]Start
@pytest.mark.asyncio
async def test_submit_success(overridden_get_db):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-add-plant/{land.code}',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True

@pytest.mark.asyncio
async def test_submit_request_validation_error(overridden_get_db):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-add-plant/{land.code}',
            json=json.dumps({"xxxx":"yyyy"}),
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 400  # Expecting validation error for incorrect data



@pytest.mark.asyncio
async def test_submit_authorization_failure_bad_api_key(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-add-plant/{land_code}',
            json={},
            headers={'API_KEY': 'xxx'}
            
        )
        assert response.status_code == 401 


@pytest.mark.asyncio
async def test_submit_authorization_failure_empty_header_key(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-add-plant/{land_code}',
            json={},
            headers={'API_KEY': ''}
            
        )
        assert response.status_code == 401 

@pytest.mark.asyncio
async def test_submit_authorization_failure_no_header(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {}
    # test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-add-plant/{land_code}', 
            json={}
            
        )
        assert response.status_code == 401 

@pytest.mark.asyncio
async def test_submit_endpoint_url_failure(overridden_get_db: AsyncSession): 
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-add-plant/{land_code}/xxxx',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 501   
        
@pytest.mark.asyncio
async def test_submit_endpoint_invalid_code_failure(overridden_get_db: AsyncSession):  
    land_code = uuid.UUID(int=0)
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.post(
            f'/api/v1_0/land-add-plant/{land_code}',
            json={},
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200 
        assert response.json()['success'] is False


@pytest.mark.asyncio
async def test_submit_endpoint_method_failure(overridden_get_db: AsyncSession): 
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-add-plant/{land_code}', 
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405
##GENLearn[isPostWithIdAvailable=true]End
##GENTrainingBlock[caseisPostWithIdAvailable]End  

@pytest.mark.asyncio
async def test_init_success(overridden_get_db: AsyncSession):
    land = await LandFactory.create_async(overridden_get_db)
    land_code = land.code
    api_dict = {'LandCode': str(land_code)}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/land-add-plant/{land_code}/init',
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
            f'/api/v1_0/land-add-plant/{land_code}/init',
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
            f'/api/v1_0/land-add-plant/{land_code}/init',
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
            f'/api/v1_0/land-add-plant/{land_code}/init' 
            
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
            f'/api/v1_0/land-add-plant/{land_code}/init/xxx',
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
            f'/api/v1_0/land-add-plant/{land_code}/init',
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
            f'/api/v1_0/land-add-plant/{land_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 405
  
def teardown_module(module):
    app.dependency_overrides.clear()