from fastapi import FastAPI

from app.middleware.http_error_handler import HTTPErrorHandler
from app.middleware.request_middleware import logging_middleware
from app.routes.v1 import example_one

app = FastAPI(
    title="Prueba api 2",
    summary="Esto es algo nuevo.",
)

app.add_middleware(HTTPErrorHandler)
app.middleware("http")(logging_middleware)

app.include_router(example_one.router)


@app.get("/")
async def root():
    return {"test": "Hola mundo! 1"}
