from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from helpers.session_context import SessionContext 
from managers import LandManager
from managers import FlavorManager
from models import Plant, Base
import configparser
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from database import get_db, engine
from starlette.exceptions import HTTPException as StarletteHTTPException
from apis.fs_farm_api.v1_0.routers import fs_farm_api_v1_0_router
import current_runtime
import logging
 
logging.basicConfig(level=logging.INFO)
logging.info('Start Main')
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


@app.get("/")
async def read_root():
	return RedirectResponse(url="/redoc")

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async for session in get_db():
        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context) 
        await session.commit()
        break
