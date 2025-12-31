# LangChain MCP Adapters POC

This is a Proof of Concept (POC) demonstrating the use of LangChain MCP Adapters to connect MCP (Model Context Protocol) tools with LangGraph agents using HTTP transport.

## Overview

This POC includes:
- **Math Server**: An MCP server providing `add` and `multiply` tools (HTTP transport)
- **Weather Server**: An MCP server providing `get_weather` tool (HTTP transport)
- **Jira Server**: An MCP server wrapping Jira REST API (HTTP transport)
- **Slack Server**: An MCP server wrapping Slack Web API (HTTP transport)
- **LangGraph Examples**: Various examples showing how to use MCP tools with LangGraph StateGraph
- **HTTP Transport Guide**: Documentation on using HTTP transport with MCP

## Prerequisites

- Python 3.8+
- OpenAI API key (set as environment variable `OPENAI_API_KEY`)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=<your_api_key>
```

On Windows:
```bash
set OPENAI_API_KEY=<your_api_key>
```

## Running the Examples

All examples use **HTTP transport** and **LangGraph StateGraph**. Each server must be started before running the client examples.

### 1. Basic Example (Single Server)

This example demonstrates using a single MCP server with LangGraph.

**First, start the math server in a separate terminal:**
```bash
python servers/math_server.py
```

**Then, in another terminal, run the client:**
```bash
python examples/client_langgraph_basic.py
```

### 2. Multiple Servers Example

This example demonstrates connecting to multiple MCP servers simultaneously with LangGraph.

**First, start the servers in separate terminals:**
```bash
# Terminal 1: Math server (port 8000)
python servers/math_server.py

# Terminal 2: Weather server (port 8001)
python servers/weather_server.py
```

**Then, in another terminal, run the client:**
```bash
python examples/client_langgraph_multi.py
```

### 3. External Services Example (Jira & Slack)

This example demonstrates using MCP servers that wrap external APIs (Jira and Slack) with LangGraph.

**First, start the servers in separate terminals:**
```bash
# Terminal 1: Jira server (port 8003)
python servers/jira_server.py

# Terminal 2: Slack server (port 8002)
python servers/slack_server.py
```

**Then, in another terminal, run the client:**
```bash
python examples/client_external_services.py
```

**Note**: These servers use HTTP transport because they wrap external REST APIs. See [HTTP Transport Guide](docs/TRANSPORT_GUIDE.md) for details.

## Project Structure

```
.
├── servers/                           # MCP server implementations (all use HTTP)
│   ├── math_server.py                # Math server (port 8000)
│   ├── weather_server.py             # Weather server (port 8001)
│   ├── jira_server.py                # Jira API wrapper (port 8001)
│   └── slack_server.py               # Slack API wrapper (port 8002)
├── examples/                          # LangGraph client examples
│   ├── client_langgraph_basic.py     # Example: Single server with LangGraph
│   ├── client_langgraph_multi.py     # Example: Multiple servers with LangGraph
│   ├── client_langgraph.py           # Example: Multiple servers with LangGraph
│   └── client_external_services.py   # Example: External services (Jira/Slack)
├── docs/                              # Documentation
│   └── TRANSPORT_GUIDE.md            # Guide: HTTP transport with MCP
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore file
└── README.md                          # This file
```

## MCP Servers

All servers in this POC use **HTTP transport** for consistency, scalability, and production-readiness.

### Math Server (`servers/math_server.py`)

Provides two tools:
- `add(a: int, b: int) -> int`: Adds two numbers
- `multiply(a: int, b: int) -> int`: Multiplies two numbers

Uses **HTTP** transport and runs on port 8000.

### Weather Server (`servers/weather_server.py`)

Provides one tool:
- `get_weather(location: str) -> str`: Returns weather information for a location

Uses **HTTP** transport and runs on port 8001.

### Jira Server (`servers/jira_server.py`)

Provides tools for Jira operations:
- `create_jira_issue()`: Create new Jira issues
- `get_jira_issue()`: Get issue details
- `search_jira_issues()`: Search issues using JQL
- `update_jira_issue()`: Update existing issues

Uses **HTTP** transport (runs on port 8003). **Why HTTP?** This server wraps the external Jira REST API, making HTTP transport ideal. See [HTTP Transport Guide](docs/TRANSPORT_GUIDE.md) for details.

### Slack Server (`servers/slack_server.py`)

Provides tools for Slack operations:
- `send_slack_message()`: Send messages to channels
- `get_slack_channels()`: List available channels
- `get_slack_channel_history()`: Get message history
- `create_slack_channel()`: Create new channels

Uses **HTTP** transport (runs on port 8002). **Why HTTP?** This server wraps the external Slack Web API, making HTTP transport the natural choice. See [HTTP Transport Guide](docs/TRANSPORT_GUIDE.md) for details.

## Features Demonstrated

- ✅ Converting MCP tools into LangChain tools
- ✅ Connecting to MCP servers via HTTP transport
- ✅ Using MCP tools with LangGraph StateGraph
- ✅ Connecting to multiple MCP servers simultaneously
- ✅ Integrating external APIs (Jira, Slack) via MCP
- ✅ Async/await patterns for MCP client sessions

## Why HTTP Transport?

**HTTP transport is used throughout this POC because:**

1. **Scalability** - Multiple clients can connect to one server
2. **Production-ready** - Suitable for service-oriented architecture
3. **External APIs** - Natural fit for wrapping REST APIs (Jira, Slack, etc.)
4. **Deployment flexibility** - Servers can run anywhere (local, cloud, containers)
5. **Service discovery** - Servers can be discovered via URL
6. **Standard protocols** - Uses well-understood HTTP/HTTPS

📖 **See [HTTP Transport Guide](docs/TRANSPORT_GUIDE.md) for comprehensive details.**

📊 **See [Transport Comparison](docs/TRANSPORT_COMPARISON.md) for differences between stdio, SSE, and streamable-http.**

## Why LangGraph?

**LangGraph is used for all examples because:**

1. **State management** - Built-in state management for complex workflows
2. **Control flow** - Explicit control flow with graphs
3. **Tool integration** - Seamless integration with MCP tools via ToolNode
4. **Production-ready** - Designed for production AI applications
5. **Flexibility** - Easy to extend and customize agent behavior

## Notes

- All servers use HTTP transport and must be started separately
- Each server runs on a different port to avoid conflicts
- All file paths are relative to the project root
- The examples use `gpt-4o` model - you can change this in the code if needed
- Jira and Slack servers include mock implementations - configure credentials for real usage
- Make sure to start the required servers before running client examples

## Server Ports

| Server | Port |
|-------|------|
| Math | 8000 |
| Weather | 8001 |
| Jira | 8003 |
| Slack | 8002 |

**Note**: Each server uses a unique port to avoid conflicts.

## Troubleshooting

1. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

2. **OpenAI API errors**: Verify your `OPENAI_API_KEY` is set correctly

3. **Server connection errors**: Make sure the required MCP servers are running on the correct ports before running client examples

4. **Port conflicts**: If a port is already in use, you can change the port in the server file or stop the conflicting service

5. **Path errors**: Make sure you're running commands from the project root directory

## References

- [LangChain MCP Adapters Documentation](https://github.com/langchain-ai/langchain-mcp-adapters)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MCP Protocol](https://modelcontextprotocol.io/)
