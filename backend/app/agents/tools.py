from app.mcp.client import get_mcp_tools

AGENT_TOOL_NAMES = {
    "google_news_feed",
    "search",
    "fetch",
}


async def get_agent_tools():
    """
    Return only the MCP tools that should be exposed
    to the LangGraph research agent.
    """

    all_tools = await get_mcp_tools()

    selected_tools = [
        tool
        for tool in all_tools
        if tool.name in AGENT_TOOL_NAMES
    ]

    return selected_tools