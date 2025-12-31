"""
MCP Server for Jira Operations
Wraps Jira REST API as MCP tools

This server uses HTTP transport because:
- It connects to external Jira API
- Multiple clients may need to connect
- It should run as a standalone service
- Production deployment requires HTTP
"""
import os
from typing import Optional
from mcp.server.fastmcp import FastMCP

# In a real implementation, you would use the Jira Python library
# from jira import JIRA

mcp = FastMCP("Jira")

# Configuration from environment variables
JIRA_SERVER = os.getenv("JIRA_SERVER", "https://your-domain.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# In production, initialize Jira client here
# jira_client = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


@mcp.tool()
async def create_jira_issue(
    project_key: str,
    summary: str,
    description: Optional[str] = None,
    issue_type: str = "Task"
) -> dict:
    """
    Create a new Jira issue.
    
    Args:
        project_key: The project key (e.g., 'PROJ')
        summary: Issue summary/title
        description: Optional issue description
        issue_type: Type of issue (Task, Bug, Story, etc.)
    
    Returns:
        Dictionary with created issue details
    """
    # In production, this would call the actual Jira API:
    # issue_dict = {
    #     'project': {'key': project_key},
    #     'summary': summary,
    #     'description': description or '',
    #     'issuetype': {'name': issue_type},
    # }
    # new_issue = jira_client.create_issue(fields=issue_dict)
    # return {"key": new_issue.key, "id": new_issue.id, "url": new_issue.permalink()}
    
    # Mock response for demonstration
    return {
        "key": f"{project_key}-123",
        "id": "12345",
        "summary": summary,
        "status": "To Do",
        "message": "Issue created successfully (mock)"
    }


@mcp.tool()
async def get_jira_issue(issue_key: str) -> dict:
    """
    Get details of a Jira issue by key.
    
    Args:
        issue_key: The issue key (e.g., 'PROJ-123')
    
    Returns:
        Dictionary with issue details
    """
    # In production:
    # issue = jira_client.issue(issue_key)
    # return {
    #     "key": issue.key,
    #     "summary": issue.fields.summary,
    #     "status": issue.fields.status.name,
    #     "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
    #     "description": issue.fields.description,
    #     "url": issue.permalink()
    # }
    
    # Mock response
    return {
        "key": issue_key,
        "summary": "Sample Issue",
        "status": "In Progress",
        "assignee": "John Doe",
        "description": "This is a sample issue",
        "url": f"{JIRA_SERVER}/browse/{issue_key}"
    }


@mcp.tool()
async def search_jira_issues(jql: str, max_results: int = 50) -> dict:
    """
    Search for Jira issues using JQL (Jira Query Language).
    
    Args:
        jql: JQL query string (e.g., 'project = PROJ AND status = "In Progress"')
        max_results: Maximum number of results to return
    
    Returns:
        Dictionary with search results
    """
    # In production:
    # issues = jira_client.search_issues(jql, maxResults=max_results)
    # return {
    #     "total": len(issues),
    #     "issues": [
    #         {
    #             "key": issue.key,
    #             "summary": issue.fields.summary,
    #             "status": issue.fields.status.name
    #         }
    #         for issue in issues
    #     ]
    # }
    
    # Mock response
    return {
        "total": 2,
        "issues": [
            {"key": "PROJ-123", "summary": "Sample Issue 1", "status": "In Progress"},
            {"key": "PROJ-124", "summary": "Sample Issue 2", "status": "To Do"}
        ]
    }


@mcp.tool()
async def update_jira_issue(issue_key: str, summary: Optional[str] = None, description: Optional[str] = None) -> dict:
    """
    Update a Jira issue.
    
    Args:
        issue_key: The issue key to update
        summary: New summary (optional)
        description: New description (optional)
    
    Returns:
        Dictionary with update status
    """
    # In production:
    # issue = jira_client.issue(issue_key)
    # if summary:
    #     issue.update(summary=summary)
    # if description:
    #     issue.update(description=description)
    # return {"key": issue_key, "status": "updated"}
    
    # Mock response
    return {
        "key": issue_key,
        "status": "updated",
        "message": "Issue updated successfully (mock)"
    }


if __name__ == "__main__":
    # HTTP transport is used because:
    # 1. This server wraps an external API (Jira)
    # 2. Multiple clients may connect to it
    # 3. It should run as a standalone service
    # 4. Production deployments require HTTP
    
    # HTTP transport on port 8003
    import os
    import uvicorn
    
    port = int(os.getenv("MCP_PORT", "8003"))
    app = mcp.http_app()
    uvicorn.run(app, host="0.0.0.0", port=port)

