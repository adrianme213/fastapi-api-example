from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.core.events import create_start_app_handler, create_stop_app_handler


def get_fastapi_app(title: str = "", debug: bool = False, version: str = "0.0.0"):
    initial_app = FastAPI(title=title, debug=debug, version=version)
    initial_app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # App Startup/Shutdown Events
    initial_app.add_event_handler("startup", create_start_app_handler(initial_app))
    initial_app.add_event_handler("shutdown", create_stop_app_handler(initial_app))

    # Exception Handlers
    initial_app.add_exception_handler(HTTPException, http_error_handler)
    initial_app.add_exception_handler(RequestValidationError, http422_error_handler)

    # Add Routes
    initial_app.include_router(api_router, prefix=API_PREFIX)

    return initial_app


app = get_fastapi_app(title=PROJECT_NAME, debug=DEBUG, version=VERSION)


@app.get("/", response_model=dict, status_code=status.HTTP_200_OK)
async def root():
    """
    Root landing message at index.
    """
    return {"message": "This is root! See /docs to view available endpoints."}


@app.get("/health", response_model=dict, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.
    """
    return {"message": "API is up and healthy."}
