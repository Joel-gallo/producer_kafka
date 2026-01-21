# API Producer
Proyecto en el que se desarrolla una API que permite simular eventos de usuarios.
Microservicio dedicado a la producción de mensajes.

El diseño es el siguiente
![](/diagrams/event.svg)

El stack tecnológico usado es:
- Python (FastAPI + Pydantic)

- API Producer Kafka

- Docker + Docker Compose

- Git


Los endpoints de la aplicación son los siguientes:
-   Events
    -   POST /event -> Permite añadir un evento a una cola de Kafka
    -   POST /events/validate -> Validación del modelo de datos
- Kafka
    - GET / ping -> Realiza una conexión de prueba para comprobar estado de cola de mensajes
- Health Check
    - GET /health -> endpoint para comprobar si la API esta en correcto funcionamiento

Validación Basic HTTP con inyección de dependencias

Conexión autogestionada por parte de FastAPI con ayuda de la logica de arranque y apagado con lifespan.
