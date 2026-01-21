from src.services.kafka import KafkaProducerService
from env_variables import KAFKA_BROKER


kafka_producer = KafkaProducerService(bootstrap_servers=KAFKA_BROKER)