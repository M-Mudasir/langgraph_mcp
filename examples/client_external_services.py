import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

Google_Calendar_MCP_URL = os.getenv("GOOGLE_CALENDAR_MCP_URL")

async def main():
    """
    Example: Using Zapier MCP tools via LangGraph.

    This connects to a Zapier-hosted MCP server over HTTP
    """

    # Initialize chat model
    model = AzureChatOpenAI(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    # Only Zapier MCP server configured
    client = MultiServerMCPClient(
        {
            "zapier": {
                "url": Google_Calendar_MCP_URL,
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
    builder.add_conditional_edges("call_model", tools_condition)
    builder.add_edge("tools", "call_model")

    graph = builder.compile()

    # Example: ask the model to use a Zapier tool
    print("Testing Zapier MCP tools with LangGraph...")
    response = await graph.ainvoke({"messages": [("user", f"Did I get an interview email in the past 2 weeks? current date is {datetime.now().strftime('%Y-%m-%d')}")]})
    print("Response:", response)

    print(response.get("messages", [])[-1].content)


if __name__ == "__main__":
    print("=" * 60)
    print("Zapier MCP Example")
    print("=" * 60)
    print()
    print("This example demonstrates HTTP transport for a Zapier MCP server.")
    print()
    print("=" * 60)
    print()
    asyncio.run(main())