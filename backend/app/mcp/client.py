import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


mcp_client = MultiServerMCPClient(
    {

        # =========================================================
        # 1. GOOGLE NEWS MCP
        # =========================================================
        "google_news": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8000/mcp",
        },


        # =========================================================
        # 2. WEB SEARCH MCP
        # =========================================================
        "web_search": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8001/mcp",
        },


        # =========================================================
        # 3. FILE SEARCH MCP
        # =========================================================
        "file_search": {
            "transport": "stdio",
            "command": "npx.cmd",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                r"D:\MCP's\File-Search-MCP\documents",
            ],
        },


        # =========================================================
        # 4. PDF TOOLS MCP
        # =========================================================
        "pdf_tools": {
            "transport": "stdio",
            "command": r"D:\MCP's\PDF-MCP-Python\.venv\Scripts\pdf-mcp.exe",
            "args": [
                "serve"
            ],
        },


        # =========================================================
        # 5. TELEGRAM MCP
        # =========================================================
        "telegram": {
            "transport": "stdio",
            "command": r"D:\MCP's\Telegram-MCP\.venv\Scripts\telegram-mcp.exe",
            "args": [],
            "env": {
                "TELEGRAM_API_ID": os.getenv(
                    "TELEGRAM_API_ID",
                    ""
                ),
                "TELEGRAM_API_HASH": os.getenv(
                    "TELEGRAM_API_HASH",
                    ""
                ),
                "TELEGRAM_SESSION_DIR": r"D:\MCP's\Telegram-MCP",
            },
        },


        # =========================================================
        # 6. FACT CHECK MCP
        # =========================================================
        "fact_check": {
            "transport": "stdio",
            "command": r"D:\MCP's\Fact-Check-MCP\.venv\Scripts\python.exe",
            "args": [
                r"D:\MCP's\Fact-Check-MCP\server.py"
            ],
        },


        # =========================================================
        # 7. RESEARCH ORGANIZER MCP
        # =========================================================
        "research_organizer": {
            "transport": "stdio",
            "command": r"D:\MCP's\Research-Organizer-MCP\.venv\Scripts\python.exe",
            "args": [
                r"D:\MCP's\Research-Organizer-MCP\server.py"
            ],
        },
    }
)


async def get_mcp_tools():
    """
    Get all tools from all connected MCP servers.
    """
    return await mcp_client.get_tools()


async def get_tool_by_name(tool_name: str):
    """
    Find a specific MCP tool by name.
    """

    tools = await get_mcp_tools()

    for tool in tools:
        if tool.name == tool_name:
            return tool

    return None