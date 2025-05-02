import os
import random
import time
import logging
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Variables de entorno
ELASTIC_USER = os.environ.get("ELASTIC_USER", "elastic")
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD", "password")
ES_PORT = os.environ.get("ES_PORT", "9200")
CA_CERT_PATH = os.environ.get("CA_CERT_PATH", "/certs/ca/ca.crt")
ES_HOST = f"https://es01:{ES_PORT}"
INDEX_NAME = "peliculas"

# Conexión a Elasticsearch
try:
    es = Elasticsearch(
        [ES_HOST],
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        verify_certs=True,
        ca_certs=CA_CERT_PATH
    )
    logger.info(f"Conectado a Elasticsearch en {ES_HOST}")
except Exception:
    logger.exception("Error al conectar con Elasticsearch")
    raise

# Mapping del índice
mapping = {
    "properties": {
        "titulo": {"type": "text"},
        "director": {"type": "keyword"},
        "genero": {"type": "keyword"},
        "anio": {"type": "integer"},
        "calificacion": {"type": "float"},
        "votos": {"type": "integer"},
        "fecha_ingreso": {"type": "date"},
        "ubicacion_origen": {"type": "geo_point"},
        "ciudad": {"type": "keyword"}
    }
}

# Crear el índice solo si no existe
try:
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, mappings=mapping)
        logger.info(f"Índice '{INDEX_NAME}' creado con mapping.")
    else:
        logger.info(f"Índice '{INDEX_NAME}' ya existe. No se crea de nuevo.")
except Exception:
    logger.exception("Error al crear/verificar el índice")
    raise

# Lista de ciudades y datos
ciudades = [
    {"name": "Madrid", "lat": 40.4168, "lon": -3.7038},
    {"name": "Barcelona", "lat": 41.3851, "lon": 2.1734},
    {"name": "Valencia", "lat": 39.4699, "lon": -0.3763},
    {"name": "Sevilla", "lat": 37.3891, "lon": -5.9845},
    {"name": "Zaragoza", "lat": 41.6488, "lon": -0.8891},
    {"name": "Málaga", "lat": 36.7213, "lon": -4.4214},
    {"name": "Bilbao", "lat": 43.2630, "lon": -2.9350},
    {"name": "Granada", "lat": 37.1773, "lon": -3.5986},
    {"name": "A Coruña", "lat": 43.3623, "lon": -8.4115},
    {"name": "Palma", "lat": 39.5696, "lon": 2.6502},
    {"name": "Vitoria", "lat": 42.8467, "lon": -2.6728}
]
generos = ["Acción", "Romance", "Suspenso", "Comedia", "Ciencia Ficción", "Drama", "Fantasía", "Terror"]
directores = ["Juan Pérez", "María López", "Carlos Sánchez", "Ana Martínez", "Luis García",
              "Laura Rodríguez", "Jorge Ramírez", "Elena Torres", "Andrés Gómez", "Sofía Castro"]


# Función para generar un documento
def generar_pelicula(i):
    ciudad = random.choice(ciudades)
    return {
        "titulo": f"Pelicula {i}",
        "director": random.choice(directores),
        "genero": random.choice(generos),
        "anio": random.randint(1990, 2022),
        "calificacion": round(random.uniform(5.0, 10.0), 1),
        "votos": random.randint(50, 1000),
        "fecha_ingreso": datetime.now().isoformat(),
        "ubicacion_origen": {"lat": ciudad["lat"], "lon": ciudad["lon"]},
        "ciudad": ciudad["name"]
    }


# Preparar bulk de 200 documentos
acciones = [
    {"_index": INDEX_NAME, "_source": generar_pelicula(i)}
    for i in range(1, 201)
]

# Insertar datos
try:
    helpers.bulk(es, acciones)
    logger.info(f"{len(acciones)} documentos insertados en '{INDEX_NAME}'.")
except Exception:
    logger.exception("Error al insertar documentos")
    raise

# Verificar conteo final
try:
    time.sleep(1)
    count = es.count(index=INDEX_NAME)["count"]
    logger.info(f"Total de documentos en índice '{INDEX_NAME}': {count}")
except Exception:
    logger.exception("Error al contar documentos")
    raise
