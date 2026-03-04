from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/probe", tags=["DEFAULT V1"])


@router.get("/probe")
async def probe_1():
    return {"test": "Hola mundo! 1"}
