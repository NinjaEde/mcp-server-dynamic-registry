from fastapi import FastAPI, Request
import uvicorn
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("docs")

@mcp.tool()
def answer(frage: str) -> str:
    """Antwortet auf eine Frage zum Thema Dokumentation."""
    return f"Antwort von Docs: {frage}"

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    frage = data.get("query", "")
    return {"antwort": answer(frage)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

