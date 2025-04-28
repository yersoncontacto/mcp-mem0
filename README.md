# MCP-Mem0 Cloud

Este repositorio contiene la imagen Docker para ejecutar un servidor MCP (Model Context Protocol) que se conecta a la API de Mem0 Cloud, permitiendo almacenar y recuperar información a través de tu cuenta de Mem0 Cloud.

## Características

- Servidor MCP que se conecta directamente a la API de Mem0 Cloud
- No requiere ejecutar una instancia local de Mem0
- Configurado para ejecutarse en el puerto 6380
- Usuario personalizable mediante variable de entorno
- Diseñado para integrarse fácilmente con n8n
- Soporte para arquitecturas ARM64 (Apple Silicon) y AMD64 (x86_64)

## Uso con Docker Compose

1. Crea un archivo `docker-compose.yml`:

```yaml
version: '3'
services:
  mcp-mem0-api:
    image: ghcr.io/yersoncontacto/mcp-mem0:latest
    container_name: mcp-mem0-api
    restart: unless-stopped
    ports:
      - "6380:6380"
    environment:
      - MEM0_API_KEY=tu_api_key_de_mem0_aquí
      - MEM0_USER_ID=tu_user_id_de_mem0
      - MEM0_API_URL=https://api.mem0.ai/v1
      - TRANSPORT=sse
      - HOST=0.0.0.0
      - PORT=6380
    networks:
      - tu-red-docker  # Usa tu red Docker existente

networks:
  tu-red-docker:
    external: true
```

2. Crea un archivo `.env` con tus credenciales:

```
MEM0_API_KEY=tu_api_key_de_mem0_aquí
MEM0_USER_ID=tu_user_id_de_mem0
MEM0_API_URL=https://api.mem0.ai/v1
TRANSPORT=sse
HOST=0.0.0.0
PORT=6380
```

3. Inicia el contenedor:

```bash
docker-compose up -d
```

## Configuración en n8n

En tu nodo de n8n Model Context Protocol:

- SSE Endpoint: `http://mcp-mem0-api:6380/sse` (si n8n está en la misma red Docker)
- O: `http://localhost:6380/sse` (si n8n está instalado fuera de Docker)

## Herramientas disponibles

Este servidor MCP proporciona cuatro herramientas principales:

1. **add_memory**: Almacenar cualquier tipo de información en tu cuenta de Mem0 Cloud
2. **get_all_memories**: Recuperar todas las memorias almacenadas en tu cuenta
3. **search_memory**: Buscar entre las memorias utilizando búsqueda semántica
4. **delete_memory**: Eliminar una memoria específica

## Requisitos

Para conectarte a la API de Mem0 Cloud, necesitas:

1. Una cuenta en Mem0 Cloud
2. Una API key de Mem0 Cloud
3. Tu User ID de Mem0 Cloud

## Diferencias con la versión anterior

Esta versión utiliza la API de Mem0 Cloud directamente, lo que ofrece varias ventajas:

- **No necesitas una base de datos local**: Todas las memorias se almacenan en tu cuenta de Mem0 Cloud.
- **No necesitas una API key de OpenAI**: Mem0 Cloud se encarga de los embeddings y la búsqueda semántica.
- **Infraestructura más simple**: No es necesario configurar PostgreSQL ni otras dependencias.
- **Sincronización automática**: Puedes acceder a tus memorias desde cualquier lugar donde uses Mem0.

## Solución de problemas

Si encuentras problemas:

1. **El servidor no arranca**: Verifica los logs con `docker logs mcp-mem0-api`
2. **n8n no puede conectarse**: Asegúrate de que las redes Docker estén correctamente configuradas
3. **Problemas con la API**: Verifica que tu API key y User ID sean correctos
4. **Problemas de arquitectura**: Esta imagen está construida para ARM64 (Apple Silicon) y AMD64 (x86_64)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request.
