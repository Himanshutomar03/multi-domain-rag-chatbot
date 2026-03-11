# Multi-Domain RAG Chatbot

FastAPI backend plus a Vite/React frontend with three domain-specific interfaces: Education, Medical, and Legal.

## Quick Start

**See [RUN.md](./RUN.md) for detailed setup instructions.**

### Quick Commands:

**Backend:**
```bash
cd multi-domain-rag-chatbot
pip install -r requirements.txt
# Create .env with GROQ_API_KEY=your_key
uvicorn src.app.main:app --reload --port 8000
```

**Frontend (new terminal):**
```bash
cd multi-domain-rag-chatbot/frontend
npm install
npm run dev
```

Then open: **http://localhost:5173**

## Backend
- Create a `.env` at the project root with `GROQ_API_KEY=<your_key>` (Hugging Face embeddings are pulled anonymously by default).
- Install deps: `pip install -r requirements.txt`.
- Run the API: `uvicorn src.app.main:app --reload --port 8000`.
- API surface:
	- `GET /health` → `{ "status": "ok" }`
	- `POST /api/chat` → body `{ "message": "your question", "domain": "education" | "medical" | "legal" }`, returns `{ "answer": str, "mode": str }` where `mode` states whether RAG or fallback GPT logic was used.

## Frontend (React + Vite)
- `cd frontend`
- Install deps: `npm install` (or `pnpm i` / `yarn`). This will install React Router for navigation.
- Start dev server: `npm run dev` (defaults to http://localhost:5173). The Vite proxy sends `/api` to port 8000.
- The frontend includes:
	- Home page with domain selection cards
	- Navigation bar to switch between domains
	- Three separate chat interfaces for Education, Medical, and Legal domains
	- Each interface has domain-specific styling and welcome messages

## Domain-Specific Features
- **Education**: General education, learning, and academic topics
- **Medical**: Medical information and health-related questions (with disclaimer about professional medical advice)
- **Legal**: Legal matters and law-related topics (with disclaimer about professional legal advice)

## Notes
- Vector stores are expected at:
	- `vectorstores/education_faiss`
	- `vectorstores/medical_faiss`
	- `vectorstores/legal_faiss`
- RAG logic for each domain lives in:
	- `src/rag_pipeline/rag_chain_education.py`
	- `src/rag_pipeline/rag_chain_medical.py`
	- `src/rag_pipeline/rag_chain_legal.py`
- The FastAPI app in `src/app/main.py` routes requests to the appropriate domain handler.
