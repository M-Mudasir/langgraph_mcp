# MCP Transport Comparison: stdio vs SSE vs streamable-http

## Overview

MCP (Model Context Protocol) supports three transport mechanisms, each with different characteristics and use cases. This document explains the differences and helps you choose the right one.

## Transport Options

### 1. stdio (Standard Input/Output)

**What it is:**
- Server runs as a subprocess launched by the client
- Communication happens through stdin/stdout pipes
- Process-based, not network-based

**Characteristics:**
- ✅ **Simple**: Easy to set up, no network configuration needed
- ✅ **Secure**: No network exposure, process isolation
- ✅ **Stateful**: Server process persists for the connection lifetime
- ❌ **Single client**: One server instance per client connection
- ❌ **Local only**: Server and client must be on the same machine
- ❌ **Not scalable**: Can't handle multiple clients efficiently

**Use Cases:**
- Local development and testing
- Simple tools that don't need network access
- Single-user scenarios
- Security-sensitive operations (no network exposure)

**Code Example:**
```python
# Server
mcp.run(transport="stdio")

# Client
client = MultiServerMCPClient({
    "math": {
        "command": "python",
        "args": ["math_server.py"],
        "transport": "stdio",
    }
})
```

**Architecture:**
```
Client Process
    │
    ├─ spawns ──> Server Subprocess
    │              │
    │              stdin/stdout pipes
    │              │
    └──────────────┘
```

---

### 2. SSE (Server-Sent Events) - **DEPRECATED**

**What it is:**
- Uses HTTP for client-to-server communication
- Uses SSE (Server-Sent Events) for server-to-client streaming
- Requires **two separate endpoints**: one for HTTP POST, one for SSE stream

**Characteristics:**
- ✅ **Network-based**: Can work over network
- ✅ **Streaming**: Supports real-time server-to-client updates
- ❌ **Complex**: Requires managing two separate endpoints
- ❌ **Deprecated**: As of MCP protocol version 2025-03-26
- ❌ **Less efficient**: More overhead than streamable-http
- ❌ **Infrastructure complexity**: Need to handle two connection types

**Status:**
⚠️ **DEPRECATED** - SSE as a standalone transport is deprecated in favor of `streamable-http`.

**Why it's deprecated:**
1. **Complexity**: Managing two endpoints adds complexity
2. **Inefficiency**: Less efficient than unified streamable-http
3. **Maintenance**: Harder to maintain and debug
4. **Future-proofing**: streamable-http is the recommended path forward

**Code Example (for reference only):**
```python
# Server
mcp.run(transport="sse", port=8000)

# Client
client = MultiServerMCPClient({
    "weather": {
        "url": "http://localhost:8000/mcp",
        "transport": "sse",
    }
})
```

**Architecture:**
```
Client
  │
  ├─ HTTP POST ──> Server (Endpoint 1: /mcp)
  │
  └─ SSE Stream ──> Server (Endpoint 2: /mcp/sse)
```

---

### 3. streamable-http (Recommended)

**What it is:**
- Modern, unified HTTP transport
- Single endpoint handles both request-response and streaming
- Supports bidirectional communication over one HTTP connection
- Incorporates SSE as an optional streaming mechanism internally

**Characteristics:**
- ✅ **Unified**: Single endpoint for all communication
- ✅ **Efficient**: More efficient than SSE
- ✅ **Scalable**: Handles multiple clients well
- ✅ **Production-ready**: Recommended for production deployments
- ✅ **Future-proof**: Current standard, actively maintained
- ✅ **Flexible**: Supports both request-response and streaming
- ✅ **Simpler**: Easier to implement and maintain than SSE

**Use Cases:**
- Production deployments
- Remote/cloud-hosted servers
- Multiple clients
- External API integrations (Jira, Slack, etc.)
- Microservices architecture
- Any network-based deployment

**Code Example:**
```python
# Server
mcp.run(transport="streamable-http", port=8000)

# Client
client = MultiServerMCPClient({
    "weather": {
        "url": "http://localhost:8000/mcp",
        "transport": "http",  # Client accepts "http" as alias
    }
})
```

**Architecture:**
```
Client
  │
  └─ HTTP (unified) ──> Server (Single endpoint: /mcp)
       │                    │
       │  Request/Response   │
       │  + Streaming       │
       └────────────────────┘
```

---

## Comparison Table

| Feature | stdio | SSE | streamable-http |
|---------|-------|-----|-----------------|
| **Network-based** | ❌ | ✅ | ✅ |
| **Multiple clients** | ❌ | ✅ | ✅ |
| **Remote deployment** | ❌ | ✅ | ✅ |
| **Production-ready** | ❌ | ⚠️ Deprecated | ✅ |
| **Complexity** | Low | High | Medium |
| **Endpoints needed** | 0 | 2 | 1 |
| **Streaming support** | ❌ | ✅ | ✅ |
| **Bidirectional** | ✅ | ⚠️ Complex | ✅ |
| **Scalability** | Low | Medium | High |
| **Maintenance** | Easy | Hard | Easy |
| **Future-proof** | ✅ | ❌ | ✅ |

---

## Why Not Just Use SSE?

### 1. **SSE is Deprecated**
- As of MCP protocol version 2025-03-26, SSE as a standalone transport is deprecated
- The MCP community is moving away from SSE in favor of streamable-http
- Using deprecated technology means:
  - No new features
  - Reduced support
  - Potential breaking changes in future versions

### 2. **Complexity**
SSE requires managing two separate endpoints:
- One for HTTP POST requests (client → server)
- One for SSE streams (server → client)

This adds complexity to:
- Server implementation
- Client implementation
- Infrastructure setup
- Debugging and monitoring

### 3. **Efficiency**
- streamable-http uses a single unified endpoint
- Less overhead than managing two separate connections
- Better resource utilization
- More efficient for high-throughput scenarios

### 4. **Unified Architecture**
streamable-http provides:
- Single endpoint for all communication
- Built-in support for both request-response and streaming
- Simpler mental model
- Easier to understand and maintain

### 5. **Future-Proofing**
- streamable-http is the current standard
- Actively maintained and improved
- All new features will target streamable-http
- Better long-term support

---

## Decision Guide

### Choose **stdio** when:
- ✅ Local development only
- ✅ Single-user scenarios
- ✅ Simple tools without network needs
- ✅ Security-sensitive (no network exposure)
- ✅ Quick prototyping

### Choose **streamable-http** when:
- ✅ Production deployments
- ✅ Multiple clients
- ✅ Remote/cloud servers
- ✅ External API integrations
- ✅ Microservices architecture
- ✅ Scalability is important
- ✅ Future-proofing matters

### Don't use **SSE** because:
- ❌ It's deprecated
- ❌ More complex than streamable-http
- ❌ Less efficient
- ❌ Not future-proof

---

## Migration Path

### From stdio to streamable-http:
```python
# Before (stdio)
mcp.run(transport="stdio")

# After (streamable-http)
mcp.run(transport="streamable-http", port=8000)
```

### From SSE to streamable-http:
```python
# Before (SSE - deprecated)
mcp.run(transport="sse", port=8000)

# After (streamable-http)
mcp.run(transport="streamable-http", port=8000)

# Client code can stay the same (uses "http" as alias)
client = MultiServerMCPClient({
    "server": {
        "url": "http://localhost:8000/mcp",
        "transport": "http",  # Works with streamable-http server
    }
})
```

---

## Summary

**For this POC and most production use cases, use `streamable-http`:**

1. ✅ **Modern standard** - Current recommended transport
2. ✅ **Unified** - Single endpoint simplifies everything
3. ✅ **Efficient** - Better performance than SSE
4. ✅ **Scalable** - Handles multiple clients well
5. ✅ **Future-proof** - Actively maintained
6. ✅ **Production-ready** - Suitable for all deployment scenarios

**Avoid SSE** - It's deprecated and more complex than streamable-http.

**Use stdio only** for local development or simple single-user tools.

---

## References

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [LangChain MCP Adapters Documentation](https://github.com/langchain-ai/langchain-mcp-adapters)
- MCP Protocol Version 2025-03-26 (SSE deprecation)

