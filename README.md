# reto_visualizacion_grupo3

## Proyecto: Visualización de datos de películas con Elasticsearch y Kibana

Este proyecto tiene como objetivo la ingestión, almacenamiento y visualización de un conjunto de datos simulados sobre películas utilizando la pila ELK (Elasticsearch, Logstash, Kibana). Se generan datos aleatorios sobre películas que se insertan en Elasticsearch y luego se visualizan mediante dashboards interactivos en Kibana.

Se ha utilizado Elasticsearch como motor de búsqueda y análisis de datos, junto con Python para la inserción de los datos simulados y Kibana como herramienta de visualización. Todo el sistema se orquesta mediante Docker Compose.

---

## Explicación de los Pasos Seguidos en el Proyecto

### 1. **Montaje del cluster de Elasticsearch**

- Se ha desplegado un clúster de 3 nodos de Elasticsearch con autenticación habilitada gracias al servicio setup en el
  docker compose.

- Se ha configurado Kibana para conectarse al clúster de forma segura.

- Se ha creado un script stop_cluster.sh que permite detener todo el clúster de forma ordenada.


### 2. **Generación e inserción del dataset**

- Se ha desarrollado un script en Python (insertar_datos.py) que:

  - Genera un conjunto de documentos simulados sobre películas con atributos como título, año, género, valoración, etc.

  - Inserta estos documentos en Elasticsearch utilizando su API REST.

  - Automatiza la creación del índice correspondiente.

### 3. **Creación del dashboard en Kibana**

- Se ha creado un dashboard personalizado en Kibana para visualizar los datos insertados.

- El dashboard contiene visualizaciones como el número total de películas, calificaciones máximas de las películas, mapa con el origen de las películas, etc.

- El dashboard se ha exportado en formato .ndjson, lo que permite importarlo fácilmente desde la interfaz de Kibana:

  - Kibana → Stack Management → Saved Objects → Import.

## Seguridad

- El clúster de Elasticsearch está configurado con autenticación y control de acceso.

- Kibana requiere credenciales (elastic / password) para acceder.


## Despliegue con Docker Compose

El sistema está preparado para ejecutarse con un único comando:

```bash
docker compose up --build
```
- El comando desplega:

  - Tres contenedores de Elasticsearch (nodos del clúster).

  - Un contenedor llamado "setup" que se encarga de la seguridad y de gestionar los certificados.

  - Un contenedor de Kibana configurado para conectarse al clúster.

  - Un contenedor de Python para ejecutar el script de inserción de datos.

---

## Instrucciones de Uso

### 1. **Requisitos Previos**

- Tener instalado [Docker](https://www.docker.com/get-started) y [Docker Compose](https://docs.docker.com/compose/install/).

### 2. **Ejecución**

```bash
git clone https://github.com/garaimg/reto_visualizacion_grupo3.git
cd reto_visualizacion_grupo3
docker compose up --build
```

- El script de inserción ejecutará automáticamente la carga de datos.


- Puedes ver el progreso de los servicios en los logs.

### 3. **Acceso a Kibana**

- Ir a http://localhost:5601.


- Iniciar sesión con elastic / password.


- Importar el dashboard desde el archivo .ndjson incluido:

  - Stack Management → Saved Objects → Import → Seleccionar el archivo.


- Explorar el dashboard.

---

## Alternativas Posibles

### 1. Otras Bases de Datos

- **InfluxDB**: más adecuada para datos de series temporales.


- **MongoDB**: buena opción si se quiere flexibilidad en el esquema de documentos.


- **PostgreSQL + Metabase**: alternativa relacional con buena interfaz de visualización.

### 2. Otros Métodos de generación de datos

- Generación en tiempo real con Kafka o Flask APIs.


- Inserción desde datasets reales en lugar de simulados.

---

## Posibles Vías de Mejora

- Añadir validación de datos antes de su inserción.


- Automatizar también la importación del dashboard mediante API de Kibana.


- Configurar alertas automáticas en Kibana.


- Añadir autenticación basada en roles.


- Incluir HTTPS para las comunicaciones entre servicios.

---

## Problemas / Retos Encontrados

- **Coordinación entre nodos del clúster**: configuración de nombres, puertos y certificados.


- **Carga masiva de datos:** evitar cuellos de botella en la inserción masiva.


- **Formato del dashboard .ndjson**: requiere ajustes específicos al importar.


- Carga masiva de datos: evitar errores de inserción por tamaño o formato.

---

## Extras y Mejoras Implementadas

- ✅ Clúster de Elasticsearch de 3 nodos con autenticación.
- ✅ Script automático para insertar datos de películas.
- ✅ Uso de un mapa en el dashboard personalizado de Kibana.
- ✅ Exportación e importación del dashboard en formato .ndjson.
- ✅ Orquestación completa con Docker Compose.
- ✅ Script de parada automática del clúster.
