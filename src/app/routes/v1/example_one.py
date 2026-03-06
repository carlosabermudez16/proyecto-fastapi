from fastapi import APIRouter, Request

from app.core.limiter import limiter

router = APIRouter(prefix="/api/v1/probe", tags=["DEFAULT V1"])


@router.get("/probe")
@limiter.limit("1000/second")
async def probe_1(request:Request):
    return {"test": "Hola mundo! 1"}
