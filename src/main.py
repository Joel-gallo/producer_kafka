from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.params import Depends
from src.api.events import router as events_router
from src.api.health import router as health_router
from src.api.kafka import router as kafka_router
from src.functions.depends import verify_basic_auth
from src.services import kafka_producer

@asynccontextmanager
async def lifespan(app):
    # Antes de que la app empiece a aceptar requests
    kafka_producer.start()

    yield  # <-- la app corre aquí

    # Despues de que la app deje de aceptar requests
    kafka_producer.stop()


app = FastAPI(title="User Events Producer", version="0.1.2", lifespan=lifespan,dependencies=[Depends(verify_basic_auth)])

app.include_router(prefix="",router=events_router,tags=["Events"])
app.include_router(prefix="",router=kafka_router,tags=["Kafka"])
app.include_router(prefix="",router=health_router,tags=["Health Check"])