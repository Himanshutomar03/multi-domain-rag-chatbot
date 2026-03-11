"""FastAPI entrypoint for the multi-domain RAG chatbot."""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum

from src.rag_pipeline.rag_chain_education import hybrid_rag as hybrid_rag_education
from src.rag_pipeline.rag_chain_medical import hybrid_rag as hybrid_rag_medical
from src.rag_pipeline.rag_chain_legal import hybrid_rag as hybrid_rag_legal


app = FastAPI(title="Multi-Domain RAG Chatbot", version="0.1.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


class Domain(str, Enum):
	education = "education"
	medical = "medical"
	legal = "legal"


class ChatRequest(BaseModel):
	message: str
	domain: Domain = Domain.education


class ChatResponse(BaseModel):
	answer: str
	mode: str


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
	message = req.message.strip()
	if not message:
		raise HTTPException(status_code=400, detail="Message cannot be empty")

	# Select the appropriate RAG function based on domain
	rag_functions = {
		Domain.education: hybrid_rag_education,
		Domain.medical: hybrid_rag_medical,
		Domain.legal: hybrid_rag_legal,
	}

	hybrid_rag_func = rag_functions.get(req.domain)
	if not hybrid_rag_func:
		raise HTTPException(status_code=400, detail=f"Invalid domain: {req.domain}")

	try:
		answer, mode = await run_in_threadpool(hybrid_rag_func, message)
	except Exception as exc:  # pragma: no cover - surfaced to client
		raise HTTPException(status_code=500, detail=str(exc)) from exc

	return ChatResponse(answer=answer, mode=mode)
