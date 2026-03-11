import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import ChatInterface from "./components/ChatInterface";
import "./styles.css";

function Navigation() {
  const location = useLocation();
  
  const navItems = [
    { path: "/education", label: "Education", color: "linear-gradient(135deg, #6cf0c2, #6b7bff)" },
    { path: "/medical", label: "Medical", color: "linear-gradient(135deg, #ff6b6b, #ff8e8e)" },
    { path: "/legal", label: "Legal", color: "linear-gradient(135deg, #4ecdc4, #44a08d)" },
  ];

  return (
    <nav className="top-nav">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <span className="nav-logo-icon">RAG</span>
          <span className="nav-logo-text">Multi-Domain Chatbot</span>
        </Link>
        <div className="nav-links">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-link ${location.pathname === item.path ? "active" : ""}`}
              style={{
                background: location.pathname === item.path ? item.color : "transparent",
                borderColor: location.pathname === item.path ? "transparent" : "rgba(255, 255, 255, 0.1)",
              }}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}

function HomePage() {
  return (
    <div className="home-page">
      <div className="home-content">
        <h1 className="home-title">Multi-Domain RAG Chatbot</h1>
        <p className="home-subtitle">Select a domain to start chatting</p>
        <div className="domain-cards">
          <Link to="/education" className="domain-card" style={{ background: "linear-gradient(135deg, rgba(108, 240, 194, 0.15), rgba(107, 123, 255, 0.15))" }}>
            <div className="domain-icon" style={{ background: "linear-gradient(135deg, #6cf0c2, #6b7bff)" }}>E</div>
            <h2>Education</h2>
            <p>Ask questions about education, learning, and academic topics</p>
          </Link>
          <Link to="/medical" className="domain-card" style={{ background: "linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(255, 142, 142, 0.15))" }}>
            <div className="domain-icon" style={{ background: "linear-gradient(135deg, #ff6b6b, #ff8e8e)" }}>M</div>
            <h2>Medical</h2>
            <p>Get information about medical topics and health-related questions</p>
          </Link>
          <Link to="/legal" className="domain-card" style={{ background: "linear-gradient(135deg, rgba(78, 205, 196, 0.15), rgba(68, 160, 141, 0.15))" }}>
            <div className="domain-icon" style={{ background: "linear-gradient(135deg, #4ecdc4, #44a08d)" }}>L</div>
            <h2>Legal</h2>
            <p>Ask questions about legal matters and law-related topics</p>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-wrapper">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/education"
            element={
              <ChatInterface
                domain="education"
                title="Education Assistant"
                subtitle="Hybrid RAG over your curated education vector store"
                placeholder="Ask a question about the education domain..."
                welcomeMessage="Ask anything in the education domain. I will route to the RAG stack and tell you how I answered."
                domainColor="linear-gradient(135deg, #6cf0c2, #6b7bff)"
              />
            }
          />
          <Route
            path="/medical"
            element={
              <ChatInterface
                domain="medical"
                title="Medical Assistant"
                subtitle="Hybrid RAG over your curated medical vector store"
                placeholder="Ask a question about the medical domain..."
                welcomeMessage="Ask anything in the medical domain. I will route to the RAG stack and tell you how I answered. Note: This is not a substitute for professional medical advice."
                domainColor="linear-gradient(135deg, #ff6b6b, #ff8e8e)"
              />
            }
          />
          <Route
            path="/legal"
            element={
              <ChatInterface
                domain="legal"
                title="Legal Assistant"
                subtitle="Hybrid RAG over your curated legal vector store"
                placeholder="Ask a question about the legal domain..."
                welcomeMessage="Ask anything in the legal domain. I will route to the RAG stack and tell you how I answered. Note: This is not a substitute for professional legal advice."
                domainColor="linear-gradient(135deg, #4ecdc4, #44a08d)"
              />
            }
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
