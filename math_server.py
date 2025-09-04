from mcp.server.fastmcp import FastMCP

print("Math MCP server started")

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

# running the server using stdio transport
if __name__ == "__main__":
    mcp.run(transport="stdio")
