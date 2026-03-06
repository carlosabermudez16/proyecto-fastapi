from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.exceptions import AppException
from app.core.limiter import limiter
from app.core.logger import logger
from app.database.init_db import create_database_if_not_exists  #, create_tables
#from app.middleware.http_error_handler import HTTPErrorHandler
from app.middleware.request_middleware import logging_middleware
from app.routes.v1 import example_one, items, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Startup logic
    create_database_if_not_exists()
    #create_tables(engine)
    print("✅ DB initialized")

    yield

    # 🛑 Shutdown logic (opcional)
    print("🛑 App shutting down")

app = FastAPI(
    title="Prueba api 2",
    summary="Esto es algo nuevo.",
    lifespan=lifespan,
)

#app.add_middleware(HTTPErrorHandler)
app.middleware("http")(logging_middleware)
app.state.limiter = limiter

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    #logger.exception(
    #    f"Unhandled error on {request.method} {request.url}"
    #)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "internal server error"},
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.exception(
        f"Application error on {request.method} {request.url} -> {exc}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


routers = [
    example_one.router,
    users.router,
    items.router,
]
for router in routers:
    app.include_router(router)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
async def root():
    return {"test": "Hola mundo! 1"}
