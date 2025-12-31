"""
MCP Server for Weather Operations
Provides weather information via MCP protocol
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather", port=8002)

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return f"It's always sunny in {location}"

mcp.run(transport="streamable-http")