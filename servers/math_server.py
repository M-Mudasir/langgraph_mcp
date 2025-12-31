"""
MCP Server for Math Operations
Provides add and multiply tools via MCP protocol

Uses HTTP transport for consistency with other servers and to support
multiple clients connecting simultaneously.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math", port=8001)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


mcp.run(transport="streamable-http")
