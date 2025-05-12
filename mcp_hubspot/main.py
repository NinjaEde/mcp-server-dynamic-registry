from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hubspot")

@mcp.tool()
def answer(frage: str) -> str:
    """Antwortet auf eine Frage zum Thema HubSpot."""
    return f"Antwort von HubSpot: {frage}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

