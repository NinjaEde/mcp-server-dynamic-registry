from fastapi import FastAPI, Request, Header
from pydantic import BaseModel
import httpx
import json
import socket
import os
from typing import List, Dict
from utils import get_kunde_by_key
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS für das Frontend erlauben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

KUNDEN_PATH = "kunden.json"

def load_kunden():
    with open(KUNDEN_PATH) as f:
        return json.load(f)

def save_kunden(kunden):
    with open(KUNDEN_PATH, "w") as f:
        json.dump(kunden, f, indent=2)

kunden = load_kunden()

class QueryRequest(BaseModel):
    query: str

class TenantCreateRequest(BaseModel):
    name: str
    api_key: str
    modules: List[str]

def discover_mcp_modules(modules: list, port: int = 8000) -> list:
    """Prüft, welche Module per DNS erreichbar sind."""
    reachable = []
    for name in modules:
        try:
            socket.gethostbyname(name)
            reachable.append(name)
        except Exception:
            continue
    return reachable

@app.get("/modules")
def list_modules():
    """List all currently discoverable MCP modules."""
    modules = discover_mcp_modules(kunden.keys())
    return {"modules": modules}

@app.get("/tenants")
def list_tenants():
    """List all tenants and their configured modules."""
    return kunden

@app.post("/tenants")
def add_tenant(req: TenantCreateRequest):
    kunden = load_kunden()
    if req.name in kunden:
        return JSONResponse(status_code=400, content={"error": "Tenant existiert bereits"})
    kunden[req.name] = {"api_key": req.api_key, "modules": req.modules}
    save_kunden(kunden)
    return {"success": True, "tenant": req.name}

@app.delete("/tenants/{tenant_name}")
def delete_tenant(tenant_name: str):
    kunden = load_kunden()
    if tenant_name not in kunden:
        return JSONResponse(status_code=404, content={"error": "Tenant nicht gefunden"})
    del kunden[tenant_name]
    save_kunden(kunden)
    return {"success": True, "deleted": tenant_name}

@app.post("/query")
async def query(request: QueryRequest, x_api_key: str = Header(...)):
    kunde, config = get_kunde_by_key(x_api_key, kunden)
    if not kunde:
        return {"error": "Ungültiger API-Key"}

    module_list = config["modules"]
    available_modules = set(discover_mcp_modules(module_list))
    antworten = []
    for modul in module_list:
        if modul not in available_modules:
            antworten.append(f"{modul}: Nicht erreichbar")
            continue
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(f"http://{modul}:8000/answer", json={"frage": request.query})
                antworten.append(f"{modul}: {res.json()['antwort']}")
        except Exception as e:
            antworten.append(f"{modul}: Fehler - {str(e)}")

    return {"kunde": kunde, "antworten": antworten}

