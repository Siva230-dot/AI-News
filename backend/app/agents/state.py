from typing import Any
from langgraph.graph import MessagesState


class ResearchState(MessagesState):

    routes: list[str]
    mcp_results: dict[str, Any]