from pathlib import Path
import os
from typing import Tuple
from dotenv import load_dotenv
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq



PROJECT_ROOT = Path(__file__).resolve().parents[2]
VS_PATH = PROJECT_ROOT / "vectorstores" / "education_faiss"


SCORE_THRESHOLD = 0.80

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from .env")
    return ChatGroq(model="llama-3.1-8b-instant", api_key=api_key)

def load_vectors():
    if not VS_PATH.exists():
        raise FileNotFoundError(f"Vector store not found at {VS_PATH}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(str(VS_PATH), embeddings, allow_dangerous_deserialization=True)

RAG_PROMPT = PromptTemplate(
    input_variables=["question", "context"],
    template="""
You are an EDUCATION domain assistant.
Use ONLY the provided context to answer.

Question:
{question}


Context:
{context}

Answer:
""",
)

GENERIC_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""
You are a helpful education assistant.
Answer the question as best as you can only related to education topics not using any external context 
and if the question is not related to education, politely inform the user that you can only answer education-related questions.
and say sorry for the inconvenience.
and if you don't know the answer, just say that you don't know. Do not try to make up an answer.
and keep the answer concise and to the point.
and use a professional and friendly tone.
and avoid using filler phrases like "As an AI language model".
and if asked about current events, inform the user that your knowledge is up to 2023 only.
if the question is about programming or coding, provide a clear and concise explanation or code snippet.
if the question is about historical events, provide accurate and relevant information based on your training data.
if question is outside education domain, politely inform the user that you can only answer education-related questions.
solve maths general questions too:


{question}

Answer:
""",
)

def hybrid_rag(question: str) -> Tuple[str, str]:
    llm = get_llm()
    vs = load_vectors()

    docs = vs.similarity_search_with_score(question, k=3)

    if not docs:
        prompt = GENERIC_PROMPT.format(question=question)
        resp = llm.invoke(prompt)
        return resp.content, "GPT (no docs)"

    best_doc, best_score = docs[0]
    print(f"Best similarity score: {best_score:.4f}")

    if best_score > SCORE_THRESHOLD:
        prompt = GENERIC_PROMPT.format(question=question)
        resp = llm.invoke(prompt)
        return resp.content, f"GPT (score={best_score:.4f} > {SCORE_THRESHOLD})"

    context = "\n\n".join(doc.page_content for doc, _ in docs)
    prompt = RAG_PROMPT.format(question=question, context=context)
    resp = llm.invoke(prompt)
    return resp.content, f"RAG (score={best_score:.4f} <= {SCORE_THRESHOLD})"


if __name__ == "__main__":
    print("Hybrid RAG (Education) – ask a question, or press Enter to exit.\n")
    while True:
        q = input("Question: ").strip()
        if not q:
            break
        try:
            answer, mode = hybrid_rag(q)
            print("\n--- MODE USED:", mode, "---")
            print(answer)
            print("\n" + "-" * 80 + "\n")
        except Exception as e:
            print("Error:", e)
