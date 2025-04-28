FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias necesarias
RUN pip install --no-cache-dir fastapi uvicorn requests pydantic python-dotenv

# Exponer el puerto
EXPOSE 6380

# Copiar archivos del proyecto
COPY src /app/src
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install -r requirements.txt

# Variables de entorno por defecto
ENV TRANSPORT=sse
ENV HOST=0.0.0.0
ENV PORT=6380
ENV MEM0_USER_ID=n8n_user

# Comando para ejecutar la aplicación
CMD ["python", "src/main.py"]
