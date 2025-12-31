"""
MCP Server for Slack Operations
Wraps Slack Web API as MCP tools

This server uses HTTP transport because:
- It connects to external Slack API
- Multiple clients may need to connect
- It should run as a standalone service
- Production deployment requires HTTP
"""
import os
from typing import Optional, List
from mcp.server.fastmcp import FastMCP

# In a real implementation, you would use the Slack SDK
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

mcp = FastMCP("Slack")

# Configuration from environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_WORKSPACE = os.getenv("SLACK_WORKSPACE", "your-workspace")

# In production, initialize Slack client here
# slack_client = WebClient(token=SLACK_BOT_TOKEN)


@mcp.tool()
async def send_slack_message(
    channel: str,
    message: str,
    thread_ts: Optional[str] = None
) -> dict:
    """
    Send a message to a Slack channel.
    
    Args:
        channel: Channel ID or name (e.g., '#general' or 'C1234567890')
        message: Message text to send
        thread_ts: Optional timestamp of parent message to reply in thread
    
    Returns:
        Dictionary with message details
    """
    # In production:
    # try:
    #     response = slack_client.chat_postMessage(
    #         channel=channel,
    #         text=message,
    #         thread_ts=thread_ts
    #     )
    #     return {
    #         "ok": True,
    #         "ts": response["ts"],
    #         "channel": response["channel"],
    #         "message": response["message"]["text"]
    #     }
    # except SlackApiError as e:
    #     return {"ok": False, "error": str(e)}
    
    # Mock response
    return {
        "ok": True,
        "ts": "1234567890.123456",
        "channel": channel,
        "message": message,
        "note": "Mock response - configure SLACK_BOT_TOKEN for real usage"
    }


@mcp.tool()
async def get_slack_channels(types: str = "public_channel,private_channel") -> dict:
    """
    Get list of Slack channels.
    
    Args:
        types: Comma-separated list of channel types (public_channel, private_channel, mpim, im)
    
    Returns:
        Dictionary with list of channels
    """
    # In production:
    # try:
    #     response = slack_client.conversations_list(types=types)
    #     return {
    #         "ok": True,
    #         "channels": [
    #             {
    #                 "id": ch["id"],
    #                 "name": ch["name"],
    #                 "is_private": ch.get("is_private", False),
    #                 "num_members": ch.get("num_members", 0)
    #             }
    #             for ch in response["channels"]
    #         ]
    #     }
    # except SlackApiError as e:
    #     return {"ok": False, "error": str(e)}
    
    # Mock response
    return {
        "ok": True,
        "channels": [
            {"id": "C1234567890", "name": "general", "is_private": False, "num_members": 100},
            {"id": "C0987654321", "name": "random", "is_private": False, "num_members": 50},
            {"id": "C1122334455", "name": "dev-team", "is_private": True, "num_members": 10}
        ]
    }


@mcp.tool()
async def get_slack_channel_history(
    channel: str,
    limit: int = 100,
    oldest: Optional[str] = None
) -> dict:
    """
    Get message history from a Slack channel.
    
    Args:
        channel: Channel ID or name
        limit: Maximum number of messages to retrieve
        oldest: Optional timestamp of oldest message to retrieve
    
    Returns:
        Dictionary with message history
    """
    # In production:
    # try:
    #     response = slack_client.conversations_history(
    #         channel=channel,
    #         limit=limit,
    #         oldest=oldest
    #     )
    #     return {
    #         "ok": True,
    #         "messages": [
    #             {
    #                 "ts": msg["ts"],
    #                 "user": msg.get("user", "unknown"),
    #                 "text": msg.get("text", ""),
    #                 "type": msg.get("type", "message")
    #             }
    #             for msg in response["messages"]
    #         ]
    #     }
    # except SlackApiError as e:
    #     return {"ok": False, "error": str(e)}
    
    # Mock response
    return {
        "ok": True,
        "messages": [
            {
                "ts": "1234567890.123456",
                "user": "U1234567890",
                "text": "Sample message 1",
                "type": "message"
            },
            {
                "ts": "1234567891.123456",
                "user": "U0987654321",
                "text": "Sample message 2",
                "type": "message"
            }
        ]
    }


@mcp.tool()
async def create_slack_channel(name: str, is_private: bool = False) -> dict:
    """
    Create a new Slack channel.
    
    Args:
        name: Channel name (lowercase, no spaces)
        is_private: Whether the channel should be private
    
    Returns:
        Dictionary with created channel details
    """
    # In production:
    # try:
    #     response = slack_client.conversations_create(
    #         name=name,
    #         is_private=is_private
    #     )
    #     return {
    #         "ok": True,
    #         "channel": {
    #             "id": response["channel"]["id"],
    #             "name": response["channel"]["name"],
    #             "is_private": response["channel"]["is_private"]
    #         }
    #     }
    # except SlackApiError as e:
    #     return {"ok": False, "error": str(e)}
    
    # Mock response
    return {
        "ok": True,
        "channel": {
            "id": "C9876543210",
            "name": name,
            "is_private": is_private
        },
        "note": "Mock response - configure SLACK_BOT_TOKEN for real usage"
    }


if __name__ == "__main__":
    # HTTP transport is used because:
    # 1. This server wraps an external API (Slack)
    # 2. Multiple clients may connect to it
    # 3. It should run as a standalone service
    # 4. Production deployments require HTTP
    
    # Streamable HTTP transport on port 8002
    import os
    import uvicorn
    
    port = int(os.getenv("MCP_PORT", "8002"))
    app = mcp.http_app()
    uvicorn.run(app, host="0.0.0.0", port=port)

