from fastapi import APIRouter
from src.services import kafka_producer

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok"
    }
