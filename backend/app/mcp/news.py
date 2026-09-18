from app.mcp.client import get_mcp_tools

async def search_news(query: str, max_results: int = 5):

    tools = await get_mcp_tools()

    google_news_tool = next(
        tool for tool in tools
        if tool.name == "google_news_feed"
    )

    result = await google_news_tool.ainvoke(
        {
            "query": query,
            "max_results": max_results,
        }
    )

    return result