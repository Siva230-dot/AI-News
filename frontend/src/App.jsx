import { useState, useRef, useEffect, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

const API_URL = "http://127.0.0.1:9000/api/chat";

const MCP_ROSTER = [
  { icon: "📰", name: "Google News MCP", purpose: "Get latest/current news" },
  { icon: "🌐", name: "MCP Web Search", purpose: "Search the web and research topics" },
  { icon: "📁", name: "File Search MCP", purpose: "Search through local documents/files" },
  { icon: "📄", name: "PDF Tools MCP", purpose: "Extract/process information from PDFs" },
  { icon: "🔍", name: "Fact Check MCP", purpose: "Verify claims using web sources" },
  { icon: "💾", name: "Research Organizer MCP", purpose: "Save and manage research results" },
  { icon: "📱", name: "Telegram MCP", purpose: "Send research/results through Telegram" },
];

function RosterScreen({ onEnter }) {
  return (
    <div className="roster-screen">
      <div className="roster-card">
        <div className="roster-header">
          <span className="masthead-mark">AI</span>
          <div>
            <h1>News Intelligence</h1>
            <p>research desk</p>
          </div>
        </div>

        <p className="roster-intro">
          Every wire on the desk is live. Here's what's connected before you file your first question.
        </p>

        <table className="roster-table">
          <thead>
            <tr>
              <th>#</th>
              <th>MCP</th>
              <th>Purpose</th>
            </tr>
          </thead>
          <tbody>
            {MCP_ROSTER.map((mcp, i) => (
              <tr key={mcp.name}>
                <td className="roster-index">{i + 1}</td>
                <td className="roster-name">
                  <span className="roster-icon">{mcp.icon}</span>
                  {mcp.name}
                </td>
                <td className="roster-purpose">{mcp.purpose}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <button className="enter-desk-btn" onClick={onEnter}>
          Enter the desk →
        </button>
      </div>
    </div>
  );
}

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function Dispatch({ message, onRetry }) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === "user";
  const isError = message.role === "error";

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  };

  return (
    <div className={`dispatch ${isUser ? "user" : isError ? "error" : "assistant"}`}>
      <div className="dispatch-meta">
        <span className="dispatch-tag">
          {isUser ? "YOU" : isError ? "DISPATCH FAILED" : "AI"}
        </span>
        <span className="dispatch-rule" />
        <span className="dispatch-time">{formatTime(message.time)}</span>
      </div>
      <div className="dispatch-body">
  {isUser ? (
    message.content
  ) : (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
          >
            {children}
          </a>
        ),
      }}
    >
      {message.content}
    </ReactMarkdown>
  )}
</div>
      {!isUser && (
        <div className="dispatch-actions">
          {isError ? (
            <button className="dispatch-action-btn" onClick={onRetry}>
              retry
            </button>
          ) : (
            <button className="dispatch-action-btn" onClick={handleCopy}>
              {copied ? "copied" : "copy"}
            </button>
          )}
        </div>
      )}
    </div>
  );
}

function App() {
  const [started, setStarted] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Wire is open. I'm your AI News Intelligence & Research Assistant — ask me anything and I'll dig in.",
      time: new Date(),
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true);
  const [lastUserMessage, setLastUserMessage] = useState(null);

  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = useCallback((behavior = "smooth") => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  }, []);

  useEffect(() => {
    if (autoScroll) scrollToBottom();
  }, [messages, loading, autoScroll, scrollToBottom]);

  // Auto-resize the textarea as the user types
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 160) + "px";
  }, [input]);

  const handleScroll = () => {
    const el = messagesContainerRef.current;
    if (!el) return;
    const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 80;
    setAutoScroll(nearBottom);
  };

  const dispatchMessage = async (userMessage) => {
    setLoading(true);
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response, time: new Date() },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "error",
          content: `Couldn't reach the desk: ${error.message}`,
          time: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMessage = input.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage, time: new Date() },
    ]);
    setLastUserMessage(userMessage);
    setInput("");
    setAutoScroll(true);
    await dispatchMessage(userMessage);
  };

  const handleRetry = async () => {
    if (!lastUserMessage || loading) return;
    setMessages((prev) => prev.filter((m) => m.role !== "error"));
    setAutoScroll(true);
    await dispatchMessage(lastUserMessage);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const handleClear = () => {
    setMessages([
      {
        role: "assistant",
        content: "Wire cleared. What's next?",
        time: new Date(),
      },
    ]);
  };

  if (!started) {
    return <RosterScreen onEnter={() => setStarted(true)} />;
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-title">
          <span className="masthead-mark">AI</span>
          <div>
            <h1>News Intelligence</h1>
            <p>research desk</p>
          </div>
        </div>
        <div className="header-actions">
          <div className="status">
            <span className="status-cursor" />
            <span className="status-text">MCPs connected</span>
          </div>
          <button className="clear-btn" onClick={handleClear}>
            clear wire
          </button>
        </div>
      </header>

      <main className="chat-container">
        <div className="messages" ref={messagesContainerRef} onScroll={handleScroll}>
          {messages.map((message, index) => (
            <Dispatch key={index} message={message} onRetry={handleRetry} />
          ))}

          {loading && (
            <div className="dispatch assistant">
              <div className="dispatch-meta">
                <span className="dispatch-tag">AI</span>
                <span className="dispatch-rule" />
                <span className="dispatch-time">filing…</span>
              </div>
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {!autoScroll && (
          <button className="scroll-to-bottom" onClick={() => { setAutoScroll(true); scrollToBottom(); }}>
            ↓ latest
          </button>
        )}

        <div className="input-wrapper">
          <div className="input-area">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="File a question..."
              rows="1"
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="send-button"
              aria-label="Send"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
          <div className="footer-text">
            AI can make mistakes. Verify important information.
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
