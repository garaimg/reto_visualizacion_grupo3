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
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD", "password")
ELASTIC_USER = "elastic"
ES_PORT = os.environ.get("ES_PORT", "9200")
CA_CERT_PATH = os.environ.get("CA_CERT_PATH", "/certs/ca/ca.crt")

# Construir el host de conexión: usamos el nombre del servicio de Elasticsearch definido en docker-compose
ES_HOST = f"https://es01:{ES_PORT}"

# Conexión a Elasticsearch
try:
    es = Elasticsearch(
        [ES_HOST],
        http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        scheme="https",
        port=int(ES_PORT),
        verify_certs=True,
        ca_certs=CA_CERT_PATH
    )
    logger.info(f"Conectado a Elasticsearch en {ES_HOST}")
except Exception as e:
    logger.error("Error al conectar a Elasticsearch", exc_info=True)
    raise e

# Nombre del índice
INDEX_NAME = "peliculas"

# Definir el mapeo (mapping) de campos para el índice
mapping = {
    "mappings": {
        "properties": {
            "titulo": {"type": "text"},
            "director": {"type": "keyword"},
            "genero": {"type": "keyword"},
            "anio": {"type": "integer"},
            "calificacion": {"type": "float"},
            "votos": {"type": "integer"},
            "fecha_ingreso": {"type": "date"}
        }
    }
}

# Crear el índice si no existe
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=mapping)
    logger.info(f"Índice '{INDEX_NAME}' creado.")
else:
    logger.info(f"Índice '{INDEX_NAME}' ya existe.")

# Listas base de datos para generar películas
generos = ["Acción", "Romance", "Suspenso", "Comedia", "Ciencia Ficción", "Drama", "Fantasía", "Terror"]
directores = ["Juan Pérez", "María López", "Carlos Sánchez", "Ana Martínez", "Luis García",
              "Laura Rodríguez", "Jorge Ramírez", "Elena Torres", "Andrés Gómez", "Sofía Castro"]

def generar_pelicula(i):
    return {
        "titulo": f"Pelicula {i}",
        "director": random.choice(directores),
        "genero": random.choice(generos),
        "anio": random.randint(1990, 2022),
        "calificacion": round(random.uniform(5.0, 10.0), 1),
        "votos": random.randint(50, 1000),
        "fecha_ingreso": datetime.now().isoformat()
    }

# Generar 200 películas
acciones = []
for i in range(1, 201):
    pelicula = generar_pelicula(i)
    accion = {
        "_index": INDEX_NAME,
        "_source": pelicula
    }
    acciones.append(accion)

# Insertar documentos usando el helper bulk
try:
    helpers.bulk(es, acciones)
    logger.info(f"Se han insertado {len(acciones)} documentos en el índice '{INDEX_NAME}'.")
except Exception as e:
    logger.error("Error al insertar documentos", exc_info=True)

# Verificar la inserción (opcional)
time.sleep(1)
try:
    res = es.count(index=INDEX_NAME)
    logger.info(f"Total de documentos en el índice: {res['count']}")
except Exception as e:
    logger.error("Error al obtener el conteo de documentos", exc_info=True)
