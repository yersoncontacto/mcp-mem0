import os
import json
import requests
from typing import Optional, Dict, Any, List
from fastapi import FastAPI
from pydantic import BaseModel
from mcp import MCP, MCPTransport
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Mem0 Cloud
MEM0_API_KEY = os.getenv("MEM0_API_KEY", "")
MEM0_USER_ID = os.getenv("MEM0_USER_ID", "n8n_user")
MEM0_API_URL = os.getenv("MEM0_API_URL", "https://api.mem0.ai/v1")

# Configuración del servidor MCP
TRANSPORT = os.getenv("TRANSPORT", "sse")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "6380"))

app = FastAPI(title="Mem0 MCP Server", 
              description="Servidor MCP para Mem0 que proporciona memoria a largo plazo a través del Model Context Protocol")

# Crear instancia MCP
if TRANSPORT == "sse":
    mcp = MCP(transport=MCPTransport.SSE)
else:
    mcp = MCP(transport=MCPTransport.STDIO)

@app.on_event("startup")
async def startup():
    if not MEM0_API_KEY:
        print("ADVERTENCIA: MEM0_API_KEY no está configurada. El servidor no podrá conectarse a Mem0 Cloud.")
    else:
        print(f"Conectando a Mem0 Cloud para el usuario {MEM0_USER_ID}...")

@mcp.tool()
async def add_memory(content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Guarda una memoria en Mem0 Cloud.
    
    Args:
        content: El contenido de texto a guardar como memoria.
        metadata: Metadatos opcionales para asociar con la memoria.
        
    Returns:
        Información sobre la memoria almacenada, incluyendo su ID.
    """
    if not MEM0_API_KEY:
        return {"error": "MEM0_API_KEY no está configurada. No se pudo guardar la memoria."}
    
    headers = {
        "Authorization": f"Bearer {MEM0_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "content": content,
        "userId": MEM0_USER_ID,
        "metadata": metadata or {}
    }
    
    try:
        response = requests.post(
            f"{MEM0_API_URL}/memories",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al guardar memoria: {str(e)}"}

@mcp.tool()
async def search_memory(query: str, threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Busca memorias en Mem0 Cloud mediante búsqueda semántica.
    
    Args:
        query: El texto de consulta para buscar.
        threshold: Umbral de similitud (entre 0 y 1).
        
    Returns:
        Lista de memorias que coinciden con la consulta.
    """
    if not MEM0_API_KEY:
        return {"error": "MEM0_API_KEY no está configurada. No se pudo buscar memorias."}
    
    headers = {
        "Authorization": f"Bearer {MEM0_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "userId": MEM0_USER_ID,
        "threshold": threshold
    }
    
    try:
        response = requests.post(
            f"{MEM0_API_URL}/memories/search",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json().get("memories", [])
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al buscar memorias: {str(e)}"}

@mcp.tool()
async def delete_memory(memory_id: str) -> Dict[str, Any]:
    """
    Elimina una memoria específica de Mem0 Cloud.
    
    Args:
        memory_id: El ID único de la memoria a eliminar.
        
    Returns:
        Resultado de la operación de eliminación.
    """
    if not MEM0_API_KEY:
        return {"error": "MEM0_API_KEY no está configurada. No se pudo eliminar la memoria."}
    
    headers = {
        "Authorization": f"Bearer {MEM0_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(
            f"{MEM0_API_URL}/memories/{memory_id}",
            headers=headers,
            params={"userId": MEM0_USER_ID}
        )
        
        response.raise_for_status()
        return {"success": True, "message": "Memoria eliminada correctamente"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al eliminar memoria: {str(e)}"}

@mcp.tool()
async def get_all_memories() -> List[Dict[str, Any]]:
    """
    Recupera todas las memorias almacenadas para el usuario actual.
    
    Returns:
        Lista de todas las memorias almacenadas.
    """
    if not MEM0_API_KEY:
        return {"error": "MEM0_API_KEY no está configurada. No se pudo recuperar las memorias."}
    
    headers = {
        "Authorization": f"Bearer {MEM0_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{MEM0_API_URL}/memories",
            headers=headers,
            params={"userId": MEM0_USER_ID}
        )
        
        response.raise_for_status()
        return response.json().get("memories", [])
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al recuperar las memorias: {str(e)}"}

# Montar la aplicación MCP en FastAPI
app.mount("/sse", mcp)

if __name__ == "__main__":
    import uvicorn
    
    if TRANSPORT == "sse":
        print(f"Iniciando servidor MCP en {HOST}:{PORT} utilizando transporte SSE")
        uvicorn.run(app, host=HOST, port=PORT)
    else:
        print("Iniciando servidor MCP utilizando transporte STDIO")
        mcp.run()
