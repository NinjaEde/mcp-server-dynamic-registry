from mcp.server.fastmcp import FastMCP

mcp = FastMCP("proalpha")

@mcp.tool()
def answer(frage: str) -> str:
    """Antwortet auf eine Frage zum Thema ProAlpha."""
    return f"Antwort von ProAlpha: {frage}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

