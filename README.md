# MCP-Mem0 para n8n

Este repositorio contiene la imagen Docker para ejecutar un servidor MCP (Model Context Protocol) que se integra con Mem0, permitiendo almacenar y recuperar información a través de n8n.

## Características

- Servidor MCP completo basado en [mcp-mem0](https://github.com/coleam00/mcp-mem0)
- Configurado para ejecutarse en el puerto 6380
- Usuario personalizable mediante variable de entorno
- Diseñado para integrarse fácilmente con n8n
- Soporte para arquitecturas ARM64 (Apple Silicon) y AMD64 (x86_64)

## Uso con Docker Compose

1. Crea un archivo `docker-compose.yml`:

```yaml
version: '3'
services:
  mcp-mem0:
    image: ghcr.io/yersoncontacto/mcp-mem0:latest
    container_name: mcp-mem0
    restart: unless-stopped
    ports:
      - "6380:6380"
    environment:
      - DEFAULT_USER_ID=n8n_user
      - LLM_PROVIDER=openai
      - LLM_API_KEY=tu_api_key_aquí
      - LLM_CHOICE=gpt-3.5-turbo
      - EMBEDDING_MODEL_CHOICE=text-embedding-3-small
      - DATABASE_URL=postgresql://usuario:contraseña@host:puerto/basededatos
    networks:
      - servarr-network  # Usa tu red Docker existente

networks:
  servarr-network:
    external: true
```

2. Crea un archivo `.env` con tus credenciales:

```
DEFAULT_USER_ID=n8n_user
LLM_PROVIDER=openai
LLM_API_KEY=tu_api_key_aquí
LLM_CHOICE=gpt-3.5-turbo
EMBEDDING_MODEL_CHOICE=text-embedding-3-small
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/basededatos
```

3. Inicia el contenedor:

```bash
docker-compose up -d
```

## Configuración en n8n

En tu nodo de n8n Model Context Protocol:

- SSE Endpoint: `http://mcp-mem0:6380/sse` (si n8n está en la misma red Docker)
- O: `http://localhost:6380/sse` (si n8n está instalado fuera de Docker)

## Herramientas disponibles

Este servidor MCP proporciona tres herramientas principales:

1. **save_memory**: Almacenar cualquier tipo de información en memoria a largo plazo
2. **get_all_memories**: Recuperar todas las memorias almacenadas
3. **search_memories**: Buscar entre las memorias utilizando búsqueda semántica

## Requisitos

Para el almacenamiento de vectores, necesitas:

1. Una base de datos PostgreSQL (puede ser una instancia local o usar un servicio como Supabase)
2. Una API key de OpenAI para los embeddings y LLM (o usar Ollama como alternativa gratuita)

### Alternativa con Ollama (sin costo)

Si prefieres no usar OpenAI, puedes configurar [Ollama](https://ollama.ai/) como alternativa gratuita:

```yaml
environment:
  - LLM_PROVIDER=ollama
  - LLM_BASE_URL=http://ollama:11434  # Si Ollama está en otro contenedor
  - LLM_CHOICE=llama3
  - EMBEDDING_MODEL_CHOICE=nomic-embed-text
```

## Solución de problemas

Si encuentras problemas:

1. **El servidor no arranca**: Verifica los logs con `docker logs mcp-mem0`
2. **n8n no puede conectarse**: Asegúrate de que las redes Docker estén correctamente configuradas
3. **Problemas con la base de datos**: Verifica que la URL de conexión es correcta y que la base de datos está accesible
4. **Problemas de arquitectura**: Esta imagen está construida para ARM64 (Apple Silicon) y AMD64 (x86_64)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request.
