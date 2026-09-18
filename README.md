# AI News Intelligence & Research Assistant

An AI-powered research assistant that provides a **single conversational interface** for news discovery, web research, document search, PDF processing, fact checking, research organization, and Telegram communication.

The system uses **Model Context Protocol (MCP)** servers to connect different capabilities and an **AI Gateway** with **Groq as the primary LLM provider** and **Hugging Face as the fallback provider**.

---

## 🚀 Features

- Single chat interface
- Automatic MCP selection
- Latest news search
- Web research
- Local document search
- PDF text extraction
- Fact checking
- Research storage
- Telegram messaging
- Multi-MCP workflows
- AI Gateway with LLM fallback
- Groq as primary provider
- Hugging Face as fallback provider
- LangGraph-based workflow orchestration
- React frontend
- FastAPI backend
- Markdown response rendering
- Source-based research

---

# 🏗️ Architecture

```text
                    SINGLE CHAT
                         │
                         ▼
                  React Frontend
                         │
                         ▼
                  FastAPI /api/chat
                         │
                         ▼
                    AI Gateway
                 ┌───────┴───────┐
                 ▼               ▼
               Groq        Hugging Face
             Primary          Fallback
                 └───────┬───────┘
                         ▼
                     AI Router
                         │
       ┌─────────┬───────┼────────┬──────────┐
       ▼         ▼       ▼        ▼          ▼
   Google News  Web    File     PDF       Fact Check
      MCP      Search  Search   Tools        MCP
                 MCP     MCP      MCP
       │         │       │        │          │
       └─────────┴───────┴────────┴──────────┘
                         │
                         ▼
                Research Organizer
                         │
                         ▼
                   Telegram MCP