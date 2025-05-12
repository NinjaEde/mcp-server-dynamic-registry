from mcp.server.fastmcp import FastMCP

mcp = FastMCP("docs")

@mcp.tool()
def answer(frage: str) -> str:
    """Antwortet auf eine Frage zum Thema Dokumentation."""
    return f"Antwort von Docs: {frage}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

