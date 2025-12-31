# MCP HTTP Transport Guide

## Overview

This POC uses **HTTP transport exclusively** for all MCP servers. HTTP transport provides the best foundation for production-ready, scalable MCP implementations.

## Why HTTP Transport?

### Advantages

1. **Scalability** - One server can handle multiple clients simultaneously
2. **Production-ready** - Suitable for service-oriented architecture and microservices
3. **External API Integration** - Natural fit for wrapping REST APIs (Jira, Slack, GitHub, etc.)
4. **Deployment Flexibility** - Servers can run anywhere:
   - Local development
   - Cloud services (AWS, Azure, GCP)
   - Containers (Docker, Kubernetes)
   - Serverless functions
5. **Service Discovery** - Servers can be discovered via URL
6. **Standard Protocols** - Uses well-understood HTTP/HTTPS
7. **Load Balancing** - Can be placed behind load balancers
8. **Authentication/Authorization** - Standard HTTP auth mechanisms
9. **Monitoring** - Easy to monitor with standard HTTP tools
10. **Debugging** - Can use standard HTTP debugging tools (curl, Postman, etc.)

### Characteristics

- **Process Model**: Server runs as a standalone service/daemon
- **Communication**: HTTP/HTTPS requests and responses
- **Lifecycle**: Server runs independently, clients connect via HTTP
- **Deployment**: Server can be deployed anywhere (local, cloud, container)
- **Scalability**: One server can handle multiple clients
- **Network**: Exposed via network (localhost or remote)

## HTTP Transport Architecture

```
┌─────────────┐         HTTP/HTTPS          ┌─────────────┐
│   Client    │ ──────────────────────────> │ MCP Server  │
│ (LangGraph) │ <────────────────────────── │  (HTTP)     │
└─────────────┘                              └─────────────┘
                                                      │
                                                      │ REST API
                                                      ▼
                                              ┌─────────────┐
                                              │  External  │
                                              │   Service  │
                                              │ (Jira/Slack)│
                                              └─────────────┘
```

## Code Pattern

### Server Implementation

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool()
async def my_tool(param: str) -> dict:
    """Tool description"""
    # Tool implementation
    return {"result": "value"}

if __name__ == "__main__":
    import os
    import uvicorn
    
    # Use http_app() to get ASGI app, then run with uvicorn
    port = int(os.getenv("MCP_PORT", "8000"))
    app = mcp.http_app()
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**Important**: The `mcp.run()` method only accepts these transport values:
- `"stdio"` - Standard input/output transport
- `"sse"` - Server-Sent Events transport
- `"streamable-http"` - Streamable HTTP transport (used in this POC)

### Client Implementation with LangGraph

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model

# Initialize model
model = init_chat_model("openai:gpt-4o")

# Connect to MCP servers via HTTP
# Note: Client accepts "http" as shorthand for "streamable-http"
client = MultiServerMCPClient({
    "my_server": {
        "url": "http://localhost:8000/mcp",
        "transport": "http",  # Client accepts "http" as alias for "streamable-http"
    }
})

# Get tools
tools = await client.get_tools()

# Build LangGraph
def call_model(state: MessagesState):
    response = model.bind_tools(tools).invoke(state["messages"])
    return {"messages": response}

builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "call_model")
builder.add_conditional_edges("call_model", tools_condition)
builder.add_edge("tools", "call_model")

graph = builder.compile()

# Use the graph
response = await graph.ainvoke({"messages": [("user", "Your query")]})
```

## Use Cases

### 1. External API Wrappers

**Perfect for**: Jira, Slack, GitHub, AWS, Azure, GCP, etc.

```python
# Example: Jira MCP Server
@mcp.tool()
async def create_jira_issue(project: str, summary: str) -> dict:
    # Calls Jira REST API
    response = await jira_client.create_issue(...)
    return response
```

**Why HTTP?** External services use REST APIs, HTTP transport is the natural fit.

### 2. Multi-Client Scenarios

**Perfect for**: Team-wide tools, shared services, production deployments

```python
# Multiple clients can connect to the same server
client1 = MultiServerMCPClient({"server": {"url": "http://server:8000/mcp", ...}})
client2 = MultiServerMCPClient({"server": {"url": "http://server:8000/mcp", ...}})
```

**Why HTTP?** One server instance can handle multiple clients simultaneously.

### 3. Microservices Architecture

**Perfect for**: Production deployments, cloud-native applications

```python
# Server can be deployed as a microservice
# - Docker container
# - Kubernetes pod
# - Serverless function
# - Cloud service
```

**Why HTTP?** Standard HTTP protocol works with all deployment platforms.

### 4. Local Development

**Perfect for**: Development, testing, prototyping

```python
# Run locally for development
import os
import uvicorn
port = int(os.getenv("MCP_PORT", "8000"))
app = mcp.http_app()
uvicorn.run(app, host="0.0.0.0", port=port)
```

**Why HTTP?** Easy to start/stop, works the same way as production.

## Best Practices

### 1. Port Management

- Use consistent port assignments
- Document port usage
- Use environment variables for port configuration

```python
import os
import uvicorn
port = int(os.getenv("MCP_PORT", "8000"))
app = mcp.http_app()
uvicorn.run(app, host="0.0.0.0", port=port)
```

### 2. Error Handling

- Implement proper error handling
- Return meaningful error messages
- Log errors for debugging

```python
@mcp.tool()
async def my_tool(param: str) -> dict:
    try:
        result = await external_api_call(param)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 3. Authentication

- Use environment variables for credentials
- Implement proper authentication
- Use HTTPS in production

```python
import os

API_KEY = os.getenv("EXTERNAL_API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### 4. Health Checks

- Implement health check endpoints
- Monitor server status
- Handle graceful shutdowns

### 5. Configuration

- Use environment variables
- Support configuration files
- Document required configuration

### 6. Logging

- Implement proper logging
- Log requests and responses (sanitize sensitive data)
- Use structured logging

```python
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
async def my_tool(param: str) -> dict:
    logger.info(f"Tool called with param: {param}")
    # ... implementation
```

## Deployment Options

### Local Development

```bash
python servers/my_server.py
```

### Docker

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "servers/my_server.py"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: mcp-server
        image: my-mcp-server:latest
        ports:
        - containerPort: 8000
```

### Cloud Services

- **AWS**: ECS, Lambda, EC2
- **Azure**: Container Instances, Functions, App Service
- **GCP**: Cloud Run, Cloud Functions, Compute Engine

## Security Considerations

1. **HTTPS in Production** - Always use HTTPS for production deployments
2. **Authentication** - Implement proper authentication mechanisms
3. **Rate Limiting** - Consider rate limiting for public APIs
4. **Input Validation** - Validate all inputs
5. **Error Messages** - Don't expose sensitive information in error messages
6. **CORS** - Configure CORS appropriately if needed
7. **Secrets Management** - Use proper secrets management (not hardcoded)

## Monitoring and Observability

1. **Health Checks** - Implement health check endpoints
2. **Metrics** - Track request counts, latency, errors
3. **Logging** - Structured logging for debugging
4. **Tracing** - Distributed tracing for complex workflows
5. **Alerts** - Set up alerts for errors and performance issues

## Example: Complete Server Setup

```python
"""
Complete MCP Server Example with HTTP Transport
"""
import os
import logging
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("MyService")

# Configuration
PORT = int(os.getenv("MCP_PORT", "8000"))
API_KEY = os.getenv("API_KEY")

@mcp.tool()
async def my_tool(param: str) -> dict:
    """
    Tool description.
    
    Args:
        param: Parameter description
    
    Returns:
        Dictionary with result
    """
    try:
        logger.info(f"Tool called with param: {param}")
        
        # Validate input
        if not param:
            return {"success": False, "error": "param is required"}
        
        # Call external API or perform operation
        result = await perform_operation(param)
        
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Error in my_tool: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting MCP server on port {PORT}")
    app = mcp.http_app()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
```

## Summary

**HTTP transport is the recommended choice for MCP servers because:**

- ✅ Scalable - Multiple clients per server
- ✅ Production-ready - Suitable for all deployment scenarios
- ✅ Standard - Uses well-understood HTTP protocol
- ✅ Flexible - Works with external APIs, microservices, cloud deployments
- ✅ Maintainable - Easy to debug, monitor, and maintain

**For all use cases in this POC, HTTP transport provides the best foundation for building production-ready MCP integrations with LangGraph.**
