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
TITLES_FILE = os.environ.get("TITLES_FILE", "/app/titles.txt")

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
        "titulo": {"type": "keyword"},
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

# Cargar títulos reales de archivo local
if os.path.exists(TITLES_FILE):
    with open(TITLES_FILE, encoding='utf-8') as f:
        titulos_reales = [line.strip() for line in f if line.strip()]
    logger.info(f"Cargados {len(titulos_reales)} títulos desde {TITLES_FILE}.")
else:
    logger.error(f"No se encontró el archivo de títulos en {TITLES_FILE}.")
    titulos_reales = []

# Validar que haya títulos
if not titulos_reales:
    raise RuntimeError(f"Se requiere al menos 1 título real en {TITLES_FILE}.")

# Usar todos los títulos disponibles
titulos = titulos_reales.copy()
random.shuffle(titulos)
logger.info(f"Se van a insertar {len(titulos)} documentos.")

# Función para generar un documento a partir de un título real
def generar_pelicula(titulo):
    ciudad = random.choice(ciudades)
    return {
        "titulo": titulo,
        "director": random.choice(directores),
        "genero": random.choice(generos),
        "anio": random.randint(1990, 2022),
        "calificacion": round(random.uniform(5.0, 10.0), 1),
        "votos": random.randint(50, 1000),
        "fecha_ingreso": datetime.now().isoformat(),
        "ubicacion_origen": {"lat": ciudad["lat"], "lon": ciudad["lon"]},
        "ciudad": ciudad["name"]
    }

# Construir bulk con todos los títulos
actions = [{"_index": INDEX_NAME, "_source": generar_pelicula(t)} for t in titulos]

# Insertar datos
try:
    helpers.bulk(es, actions)
    logger.info(f"{len(actions)} documentos insertados en '{INDEX_NAME}'.")
except Exception:
    logger.exception("Error al insertar documentos")
    raise

# Verificar conteo final
time.sleep(1)
try:
    count = es.count(index=INDEX_NAME)["count"]
    logger.info(f"Total de documentos en índice '{INDEX_NAME}': {count}")
except Exception:
    logger.exception("Error al contar documentos")
    raise
