from langgraph.graph import StateGraph, START, END

from app.agents.state import ResearchState
from app.agents.nodes import (
    router_node,
    mcp_node,
    synthesis_node,
)


async def build_research_agent():

    graph = StateGraph(ResearchState)

    graph.add_node(
        "router",
        router_node
    )

    graph.add_node(
        "mcp",
        mcp_node
    )

    graph.add_node(
        "synthesis",
        synthesis_node
    )

    graph.add_edge(
        START,
        "router"
    )

    graph.add_edge(
        "router",
        "mcp"
    )

    graph.add_edge(
        "mcp",
        "synthesis"
    )

    graph.add_edge(
        "synthesis",
        END
    )

    return graph.compile()