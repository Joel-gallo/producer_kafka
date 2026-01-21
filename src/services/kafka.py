import json
from time import time
from fastapi.logger import logger
from kafka import KafkaProducer
from kafka.errors import KafkaError


class KafkaProducerService:
    def __init__(self, bootstrap_servers: list[str]):
        self._bootstrap_servers = bootstrap_servers
        self._producer: KafkaProducer | None = None

    def start(self):
        if self._producer:
            return

        self._producer = KafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda v: v.encode("utf-8") if v else None,
            acks="all",
            retries=3,
            linger_ms=5,
            #api_version=(3, 6, 0)
        )

        logger.info("Kafka producer started")

    def stop(self):
        if self._producer:
            self._producer.flush()
            self._producer.close()
            logger.info("Kafka producer stopped")

    def send(self, topic: str, value: dict, key: str | None = None):
        if not self._producer:
            raise RuntimeError("Kafka producer not started")

        future = self._producer.send(
            topic=topic,
            key=key,
            value=value
        )

        # Bloqueante hasta confirmación
        future.get(timeout=10)
    
    def ping(self) -> bool:
        """
        Verifica que Kafka acepta mensajes y confirma (acks).
        """
        if not self._producer:
            return False

        try:
            future = self._producer.send(
                topic="healthcheck",
                key="ping",
                value={
                    "type": "ping",
                    "timestamp": time(),
                }
            )

            # Espera ACK del broker
            future.get(timeout=5)
            return True

        except KafkaError as ke:
            logger.error(f"Kafka error in ping: {ke}")
            return False
        except Exception as e:
            logger.error(f"Error in ping: {e}")
            return False