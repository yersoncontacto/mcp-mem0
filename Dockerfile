FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias necesarias
RUN pip install --no-cache-dir uv

# Instalar git para clonar el repositorio
RUN apt-get update && apt-get install -y git

# Clonar el repositorio
RUN git clone https://github.com/coleam00/mcp-mem0.git /app

# Configurar entorno virtual e instalar dependencias
RUN pip install -e .

# Modificar el DEFAULT_USER_ID para poder configurarlo mediante variable de entorno
RUN sed -i 's/DEFAULT_USER_ID = "user"/DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "n8n_user")/g' src/main.py

# Exponer el puerto
EXPOSE 6380

# Variables de entorno por defecto
ENV TRANSPORT=sse
ENV HOST=0.0.0.0
ENV PORT=6380
ENV DEFAULT_USER_ID=n8n_user

# Comando para ejecutar la aplicación
CMD ["python", "src/main.py"]
