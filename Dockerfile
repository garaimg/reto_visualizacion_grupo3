# Usa la imagen oficial de Python 3.9 slim como base
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y lo instala
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el script de inserción al contenedor
COPY insertar_datos.py .

# Define el comando por defecto para ejecutar el script
CMD ["python3", "insertar_datos.py"]
