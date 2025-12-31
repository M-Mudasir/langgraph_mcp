"""
Example: Using MCP tools with LangGraph StateGraph (Multiple Servers)
Demonstrates connecting to multiple MCP servers via HTTP transport
"""
import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import AzureChatOpenAI


async def main():
    """
    This example demonstrates using multiple MCP servers with LangGraph.
    All servers use HTTP transport and run on different ports.
    """

    model = AzureChatOpenAI(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        base_url=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
    )
    client = MultiServerMCPClient(
        {
            "math": {
                "url": "http://localhost:8001/mcp",
                "transport": "http",
            },
            "weather": {
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
    
    # Test math operations
    print("Testing math operations with LangGraph...")
    math_response = await graph.ainvoke({"messages": [("user", "what's (3 + 5) x 12?")]})
    print("Math Response:", math_response)
    print()
    
    # Test weather operations
    print("Testing weather operations with LangGraph...")
    weather_response = await graph.ainvoke({"messages": [("user", "what is the weather in nyc?")]})
    print("Weather Response:", weather_response)


if __name__ == "__main__":
    
    print("Note: Make sure both servers are running:")
    print("  - Math server: python servers/math_server.py (port 8001)")
    print("  - Weather server: python servers/weather_server.py (port 8002)")
    print()
    
    asyncio.run(main())

