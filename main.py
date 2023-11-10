from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker 
from managers import LandManager
from managers import FlavorManager
from models import Plant
import configparser
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from database import get_db
from starlette.exceptions import HTTPException as StarletteHTTPException
from apis.fs_farm_api.v1_0.routers import fs_farm_api_v1_0_router
 

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
    if exc.status_code == 403:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized."}
        )
    if exc.status_code == 422:
        return JSONResponse(
            status_code=400,
            content={"message": "Bad Request. Schema Failure."}
        )
    # You can add more custom handling for other status codes if needed
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.router.on_startup.append
async def startup_event():
    async with get_db() as session:
        land_manager = LandManager(session)
        flavor_manager = FlavorManager(session)
        await land_manager.create()
        await flavor_manager.create(name='unknown')
        await flavor_manager.create(name='sweet')
        await flavor_manager.create(name='sour')
