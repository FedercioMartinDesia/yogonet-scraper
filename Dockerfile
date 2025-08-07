# Usa una imagen oficial de Python
FROM python:3.12-slim


# No generar archivos pyc y mostrar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copia las dependencias primero (mejor para el cache)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia tu código fuente
COPY app/ ./app/

# Comando por defecto al iniciar el contenedor
ENTRYPOINT ["python", "-u", "app/main.py"]
