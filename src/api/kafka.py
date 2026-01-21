from fastapi import APIRouter
from src.services import kafka_producer

router = APIRouter()


@router.get("/ping")
def ping():
    kafka_ok = kafka_producer.ping()
    return {
        "kafka_status": "connected" if kafka_ok else "down"
    }
