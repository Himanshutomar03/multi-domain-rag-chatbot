import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { Message } from "../types";
import "../styles.css";

const apiBase = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");

interface ChatInterfaceProps {
  domain: "education" | "medical" | "legal";
  title: string;
  subtitle: string;
  placeholder: string;
  welcomeMessage: string;
  domainColor: string;
}

interface ChatMeta {
  sending: boolean;
  error: string | null;
}

const ChatBubble = ({ message }: { message: Message }) => {
  return (
    <div className={`bubble ${message.role}`}>
      {message.mode && (
        <div className="meta">
          <span className="tag">{message.mode}</span>
          <span>{new Date(message.timestamp ?? Date.now()).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
        </div>
      )}
      <div>{message.content}</div>
    </div>
  );
};

export default function ChatInterface({ domain, title, subtitle, placeholder, welcomeMessage, domainColor }: ChatInterfaceProps) {
  const starter: Message = {
    id: `assistant-${domain}-hello`,
    role: "assistant",
    content: welcomeMessage,
    mode: "system",
    timestamp: Date.now(),
  };

  const [messages, setMessages] = useState<Message[]>([starter]);
  const [draft, setDraft] = useState("");
  const [meta, setMeta] = useState<ChatMeta>({ sending: false, error: null });
  const listRef = useRef<HTMLDivElement | null>(null);

  const endpoint = useMemo(() => `${apiBase || ""}/api/chat`, []);

  useEffect(() => {
    const el = listRef.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }, [messages]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!draft.trim() || meta.sending) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: draft.trim(),
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setDraft("");
    setMeta({ sending: true, error: null });

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content, domain }),
      });

      if (!res.ok) {
        const detail = await res.json().catch(() => ({}));
        throw new Error(detail.detail || "Request failed");
      }

      const data = await res.json();
      const botMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: data.answer,
        mode: data.mode,
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, botMessage]);
      setMeta({ sending: false, error: null });
    } catch (err) {
      setMeta({ sending: false, error: err instanceof Error ? err.message : "Unexpected error" });
    }
  };

  return (
    <div className="app-shell">
      <header className="header">
        <div className="brand">
          <div className="logo" style={{ background: domainColor }}>
            {domain.charAt(0).toUpperCase()}
          </div>
          <div>
            <h1>{title}</h1>
            <p className="subtitle">{subtitle}</p>
          </div>
        </div>
        <span className="status-pill">
          <span className="dot" style={{ background: domainColor }} />
          Live
        </span>
      </header>

      <div className="chat-window">
        <div className="messages" ref={listRef}>
          {messages.map((m) => (
            <ChatBubble key={m.id} message={m} />
          ))}
        </div>
      </div>

      <form className="footer" onSubmit={handleSubmit}>
        <div>
          <input
            className="input"
            placeholder={placeholder}
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            disabled={meta.sending}
          />
          <div className="helper">
            {meta.error ? <span className="error">{meta.error}</span> : "Responses will note whether RAG or GPT was used."}
          </div>
        </div>
        <button className="button" type="submit" disabled={meta.sending} style={{ background: domainColor }}>
          {meta.sending ? "Thinking…" : "Send"}
        </button>
      </form>
    </div>
  );
}

