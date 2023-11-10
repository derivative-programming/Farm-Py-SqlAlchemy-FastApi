import uuid
import pytest
from httpx import AsyncClient
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from helpers.api_token import ApiToken
from models.factory. import Factory
from .conftest import overridden_get_db
from .....models.factory.plant_user_delete  import PlantUserDeletePostModelRequestFactory
from ...routers import fs_farm_api_v1_0_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
# from main import app

app = FastAPI()

app.include_router(fs_farm_api_v1_0_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=501,
            content={"message": "This is not implemented."}
        )
    # You can add more custom handling for other status codes if needed
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Override the get_db dependency for all tests in this module
# app.dependency_overrides[get_db] = overridden_get_db

# @pytest.fixture(scope="module")
# def invalid_request_data():
#     return {"xxxxxx": "yyyyy"}

# @pytest.fixture(scope="module")
# def valid_header():
#     # Replace with your actual token generation logic
#     api_dict = {'PlantCode': str(.code), 'role_name_csv': 'User'}
#     test_api_key = ApiToken.create_token(api_dict, 1)
#     return {'API_KEY': test_api_key}

# @pytest.mark.asyncio
# async def test_post_not_implemented(overridden_get_db):
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.post(
#             '/api/v1_0/plant-user-delete/',
#             json=valid_request_data,
#             headers=valid_header
#         )
#         assert response.status_code == 501

# @pytest.mark.asyncio
# async def test_submit_success(overridden_get_db):
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.post(
#             f'/api/v1_0/plant-user-delete/{.code}/',
#             json=valid_request_data,
#             headers=valid_header
#         )
#         assert response.status_code == 200
#         assert response.json()['success'] is True

# @pytest.mark.asyncio
# async def test_submit_failure(overridden_get_db, invalid_request_data, valid_header, ):
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.post(
#             f'/api/v1_0/plant-user-delete/{.code}/',
#             json=invalid_request_data,
#             headers=valid_header
#         )
#         assert response.status_code == 422  # Expecting validation error for incorrect data

# @pytest.mark.asyncio
# async def test_submit_failure2(overridden_get_db, valid_header):
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get(
#             '/api/v1_0/plant-user-delete/xxx/',
#             headers=valid_header
#         )
#         assert response.status_code == 404

@pytest.mark.asyncio
async def test_init_success(overridden_get_db: AsyncSession):
    plant_code = uuid.UUID(int=0)
    api_dict = {'PlantCode': str(plant_code), 'role_name_csv': 'User'}
    test_api_key = ApiToken.create_token(api_dict, 1)
    async with AsyncClient(app=app, base_url="http://test") as ac:

        app.dependency_overrides[get_db] = lambda: overridden_get_db
        response = await ac.get(
            f'/api/v1_0/plant-user-delete/{plant_code}/init',
            headers={'API_KEY': test_api_key}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True

@pytest.mark.asyncio
async def test_init_failure():
    plant_code = uuid.UUID(int=0)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            '/api/v1_0/plant-user-delete/{plant_code}/initxxx/'
        )
        assert response.status_code == 501

# Add any additional test cases for different scenarios and edge cases

# Add this at the end of your test module
def teardown_module(module):
    app.dependency_overrides.clear()