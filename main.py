# main.py

"""
This is the main module of the Farm-Py-SqlAlchemy-FastApi application.
It contains the FastAPI application setup,
exception handlers, and startup event.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import current_runtime
from database import get_db, engine
from helpers.session_context import SessionContext
from models import Base
from apis.fs_farm_api.v1_0.routers import fs_farm_api_v1_0_router

# Define a proper date format string
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configure the logging with a proper date format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt=DATE_FORMAT
)


logging.info('Start Main')

app = FastAPI()

app.include_router(fs_farm_api_v1_0_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):  # pylint: disable=unused-argument
    """
    Exception handler for RequestValidationError.

    Args:
        request (Request): The incoming request.
        exc (RequestValidationError): The raised exception.

    Returns:
        JSONResponse: The JSON response with error details.
    """
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):  # pylint: disable=unused-argument
    """
    Exception handler for StarletteHTTPException.

    Args:
        request (Request): The incoming request.
        exc (StarletteHTTPException): The raised exception.

    Returns:
        JSONResponse: The JSON response with error details.
    """
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

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/")
async def read_root():
    """
    Root endpoint of the application.

    Returns:
        RedirectResponse: Redirects to the API documentation.
    """
    return RedirectResponse(url="/redoc")


@app.on_event("startup")
async def startup_event():
    """
    Startup event of the application.
    Performs necessary initialization tasks.

    Returns:
        None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in get_db():
        session_context = SessionContext({}, session)
        await current_runtime.initialize(session_context)
        await session.commit()
        break
