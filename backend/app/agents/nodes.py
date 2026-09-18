import json

from app.agents.state import ResearchState
from app.agents.router import detect_routes, clean_query
from app.mcp.client import get_tool_by_name
from app.gateway.gateway import gateway


SYSTEM_MESSAGE = """
You are an AI News Intelligence & Research Assistant.

You answer the user's request using the research data
provided by the backend MCP tools.

Rules:

- Do not invent information.
- Use the provided MCP results as evidence.
- Clearly distinguish facts from uncertainty.
- When sources are available, mention them.
- Give concise but useful answers.
- If multiple sources disagree, explain the disagreement.
"""


async def router_node(state: ResearchState):

    user_message = state["messages"][-1].content

    routes = detect_routes(user_message)

    print(f"AI Router selected: {routes}")

    return {
        "routes": routes
    }


async def mcp_node(state: ResearchState):

    user_message = state["messages"][-1].content

    routes = state.get("routes", [])

    query = clean_query(user_message)

    results = {}

    # --------------------------------------------------
    # GOOGLE NEWS
    # --------------------------------------------------

    if "google_news" in routes:

        tool = await get_tool_by_name("google_news_feed")

        if tool:
            try:
                result = await tool.ainvoke({
                    "query": query,
                    "max_results": 5,
                })

                results["Google News"] = result

            except Exception as e:
                results["Google News"] = {
                    "error": str(e)
                }

    # --------------------------------------------------
    # WEB SEARCH
    # --------------------------------------------------

    if "web_search" in routes:

        tool = await get_tool_by_name("search")

        if tool:
            try:
                result = await tool.ainvoke({
                    "query": query,
                })

                results["Web Search"] = result

            except Exception as e:
                results["Web Search"] = {
                    "error": str(e)
                }

    # --------------------------------------------------
    # FILE SEARCH
    # --------------------------------------------------

    if "file_search" in routes:

        tool = await get_tool_by_name("search_files")

        if tool:
            try:

                result = await tool.ainvoke({
                    "path": r"D:\MCP's\File-Search-MCP\documents",
                    "pattern": query,
                })

                results["File Search"] = result

            except Exception as e:
                results["File Search"] = {
                    "error": str(e)
                }

    # --------------------------------------------------
    # PDF
    # --------------------------------------------------

    if "pdf" in routes:

        tool = await get_tool_by_name("extract_text")

        if tool:

            # Look for a PDF path in the message
            pdf_match = None

            for word in user_message.split():

                if word.lower().endswith(".pdf"):
                    pdf_match = word.strip("\"'")

            if pdf_match:

                try:

                    result = await tool.ainvoke({
                        "pdf_path": pdf_match
                    })

                    results["PDF Tools"] = result

                except Exception as e:
                    results["PDF Tools"] = {
                        "error": str(e)
                    }

            else:

                results["PDF Tools"] = {
                    "message": "Please provide the PDF file path."
                }

    # --------------------------------------------------
    # FACT CHECK
    # --------------------------------------------------

    if "fact_check" in routes:

        tool = await get_tool_by_name("fact_check")

        if tool:

            try:

                result = await tool.ainvoke({
                    "claim": query,
                    "max_results": 3,
                })

                results["Fact Check"] = result

            except Exception as e:

                results["Fact Check"] = {
                    "error": str(e)
                }

    # --------------------------------------------------
    # RESEARCH ORGANIZER
    # --------------------------------------------------

    if "research_organizer" in routes:

        tool = await get_tool_by_name("save_research")

        if tool:

            try:

                result = await tool.ainvoke({
                    "title": "Research",
                    "query": query,
                    "summary": user_message,
                    "sources": "[]",
                })

                results["Research Organizer"] = result

            except Exception as e:

                results["Research Organizer"] = {
                    "error": str(e)
                }

    # --------------------------------------------------
    # TELEGRAM
    # --------------------------------------------------

    if "telegram" in routes:

        tool = await get_tool_by_name("send_message")

        if tool:

            results["Telegram"] = {
                "message": (
                    "Telegram request detected. "
                    "Use the Telegram endpoint for sending."
                )
            }

    return {
        "mcp_results": results
    }


async def synthesis_node(state: ResearchState):

    user_message = state["messages"][-1].content

    mcp_results = state.get("mcp_results", {})

    # No MCP needed
    if not mcp_results:

        messages = [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

    else:

        research_data = json.dumps(
            mcp_results,
            ensure_ascii=False,
            default=str,
        )

        # Keep prompt reasonably small
        research_data = research_data[:30000]

        messages = [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": f"""
User request:

{user_message}

MCP research results:

{research_data}

Using the MCP results above, answer the user's request.
""",
            },
        ]

    response = await gateway.generate(messages)

    return {
        "messages": [
            {
                "role": "assistant",
                "content": response,
            }
        ]
    }