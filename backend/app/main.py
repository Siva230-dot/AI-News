from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.agents.research_agent import build_research_agent
from app.mcp.client import (
    get_mcp_tools,
    get_tool_by_name,
)


app = FastAPI(
    title="AI News Intelligence API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

research_agent = None


# ============================================================
# REQUEST MODELS
# ============================================================

class ChatRequest(BaseModel):

    message: str


class TelegramRequest(BaseModel):

    recipient: str

    message: str

    timeout: int = 30


class SaveResearchRequest(BaseModel):

    title: str

    query: str

    summary: str

    sources: str = "[]"


class FileSearchRequest(BaseModel):

    query: str


class PDFRequest(BaseModel):

    path: str

class FactCheckRequest(BaseModel):

    claim: str


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event():

    global research_agent

    research_agent = await build_research_agent()

    print(
        "Research Agent initialized successfully."
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():

    return {
        "status": "running",
        "service": "AI News Intelligence API",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/api/health")
async def health():

    return {
        "status": "healthy",
        "agent": research_agent is not None,
    }


# ============================================================
# LIST MCP TOOLS
# ============================================================

@app.get("/api/mcp/tools")
async def list_mcp_tools():

    tools = await get_mcp_tools()

    return {
        "count": len(tools),

        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
            }

            for tool in tools
        ],
    }


# ============================================================
# CHAT / RESEARCH AGENT
# ============================================================

@app.post("/api/chat")
async def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    if research_agent is None:
        raise HTTPException(
            status_code=503,
            detail="Research agent is not initialized."
        )

    result = await research_agent.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": request.message
            }
        ]
    })

    final_message = result["messages"][-1]

    return {
        "response": final_message.content
    }


# ============================================================
# FILE SEARCH MCP
# ============================================================

@app.post("/api/files/search")
async def search_files(
    request: FileSearchRequest
):

    tool = await get_tool_by_name(
        "search_files"
    )

    if tool is None:
        raise HTTPException(
            status_code=404,
            detail="File Search MCP tool not found."
        )

    result = await tool.ainvoke(
        {
            "path": r"D:\MCP's\File-Search-MCP\documents",
            "pattern": request.query,
        }
    )

    return {
        "result": result
    }


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

@app.post("/api/pdf/extract-text")
async def extract_pdf_text(
    request: PDFRequest
):

    tool = await get_tool_by_name(
        "extract_text"
    )

    if tool is None:
        raise HTTPException(
            status_code=404,
            detail="PDF extract_text tool not found."
        )

    result = await tool.ainvoke(
        {
            "pdf_path": request.path
        }
    )

    return {
        "result": result
    }


# ============================================================
# TELEGRAM
# ============================================================

@app.post("/api/telegram/send")
async def send_telegram(
    request: TelegramRequest
):

    tool = await get_tool_by_name(
        "send_message"
    )

    if tool is None:
        raise HTTPException(
            status_code=404,
            detail="Telegram MCP tool not found."
        )

    result = await tool.ainvoke(
        {
            "bot": request.recipient,
            "message": request.message,
            "timeout": 30,
        }
    )

    return {
        "success": True,
        "result": result
    }


# ============================================================
# SAVE RESEARCH
# ============================================================

@app.post("/api/research/save")
async def save_research(
    request: SaveResearchRequest
):

    tool = await get_tool_by_name(
        "save_research"
    )

    if tool is None:

        raise HTTPException(
            status_code=404,
            detail="Research Organizer MCP not found."
        )

    result = await tool.ainvoke(
        {
            "title": request.title,
            "query": request.query,
            "summary": request.summary,
            "sources": request.sources,
        }
    )

    return {
        "result": result
    }


# ============================================================
# LIST SAVED RESEARCH
# ============================================================

@app.get("/api/research")
async def list_research():

    tool = await get_tool_by_name(
        "list_research"
    )

    if tool is None:

        raise HTTPException(
            status_code=404,
            detail="Research Organizer MCP not found."
        )

    result = await tool.ainvoke(
        {
            "limit": 20
        }
    )

    return {
        "result": result
    }

@app.post("/api/fact-check")
async def fact_check(
    request: FactCheckRequest
):

    if not request.claim.strip():

        raise HTTPException(
            status_code=400,
            detail="Claim cannot be empty."
        )

    tool = await get_tool_by_name(
        "fact_check"
    )

    if tool is None:

        raise HTTPException(
            status_code=404,
            detail="Fact Check MCP tool not found."
        )

    result = await tool.ainvoke(
        {
            "claim": request.claim,
            "max_results": 3
        }
    )

    return {
        "claim": request.claim,
        "result": result
    }