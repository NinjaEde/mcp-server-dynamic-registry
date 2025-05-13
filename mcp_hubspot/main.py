from fastapi import FastAPI, Request
import uvicorn
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("hubspot")

@mcp.tool()
def answer(frage: str) -> str:
    """Antwortet auf eine Frage zum Thema HubSpot."""
    return f"Antwort von HubSpot: {frage}"

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    frage = data.get("query", "")
    return {"antwort": answer(frage)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

