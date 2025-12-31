"""
Example: Using MCP tools with external services (Jira and Slack) via LangGraph
Demonstrates HTTP transport for external API integrations with LangGraph StateGraph
"""
import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model


async def main():
    """
    This example demonstrates connecting to external service MCP servers using LangGraph.
    
    These servers use HTTP transport because:
    1. They wrap external REST APIs (Jira, Slack)
    2. Multiple clients may need to connect
    3. They run as standalone services
    4. Production deployments require HTTP
    
    Before running:
    1. Start Jira server: python servers/jira_server.py (runs on port 8003)
    2. Start Slack server: python servers/slack_server.py (runs on port 8002)
    3. Set environment variables:
       - JIRA_SERVER, JIRA_EMAIL, JIRA_API_TOKEN (for Jira)
       - SLACK_BOT_TOKEN (for Slack)
    """
    
    # Initialize chat model
    model = init_chat_model("openai:gpt-4o")
    
    client = MultiServerMCPClient(
        {
            "jira": {
                "url": "http://localhost:8003/mcp",
                "transport": "http",
            },
            "slack": {
                "url": "http://localhost:8002/mcp",
                "transport": "http",
            }
        }
    )
    
    tools = await client.get_tools()

    def call_model(state: MessagesState):
        response = model.bind_tools(tools).invoke(state["messages"])
        return {"messages": response}

    # Build the graph
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    
    graph = builder.compile()
    
    # Test Jira operations
    print("Testing Jira operations with LangGraph...")
    print("Note: These are mock responses. Configure Jira credentials for real usage.")
    jira_response = await graph.ainvoke({
        "messages": [("user", "Create a Jira issue in project PROJ with summary 'Fix login bug'")]
    })
    print("Jira Response:", jira_response)
    print()
    
    # Test Slack operations
    print("Testing Slack operations with LangGraph...")
    print("Note: These are mock responses. Configure Slack token for real usage.")
    slack_response = await graph.ainvoke({
        "messages": [("user", "Send a message to #general channel saying 'Hello from MCP!'")]
    })
    print("Slack Response:", slack_response)


if __name__ == "__main__":
    # Make sure OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        exit(1)
    
    print("=" * 60)
    print("External Services MCP Example")
    print("=" * 60)
    print()
    print("This example demonstrates HTTP transport for external services.")
    print()
    print("Prerequisites:")
    print("1. Start Jira server: python servers/jira_server.py")
    print("2. Start Slack server: python servers/slack_server.py")
    print("3. Optional: Set JIRA_* and SLACK_* environment variables")
    print()
    print("=" * 60)
    print()
    
    asyncio.run(main())

