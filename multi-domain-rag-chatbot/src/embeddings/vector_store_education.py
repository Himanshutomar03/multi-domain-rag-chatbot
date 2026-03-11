import json
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

RAW_PATH = "data/processed/education/processed_1.jsonl"
FAISS_STORE_PATH = "vectorstores/education_faiss"
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def load_docs(raw_path: str = RAW_PATH):
    raw_path = Path(raw_path)
    if not raw_path.is_absolute():
        
        raw_path = (PROJECT_ROOT / raw_path).resolve()
    
    docs = []
    with raw_path.open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            text = item.get("context", "")
            metadata = {"title": item.get("title", "")}
            docs.append(Document(page_content=text, metadata=metadata))
    
    print(f"Loaded {len(docs)} base documents")
    return docs

def create_vec_education():
    jsonl_path = (PROJECT_ROOT / RAW_PATH).resolve()
    vs_path = (PROJECT_ROOT / FAISS_STORE_PATH).resolve()

    print("Project root:", PROJECT_ROOT)
    print("Using JSONL:", jsonl_path)
    print("Vector store dir:", vs_path)
    
    if not jsonl_path.exists():
        raise FileNotFoundError(f"Processed JSONL not found at {jsonl_path}")
    
    docs = load_docs(jsonl_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    split_docs = text_splitter.split_documents(docs)
    print(f"Split into {len(split_docs)} chunks")

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(split_docs, embedding_model)
    
    vs_path.parent.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(vs_path))
    print(f"Vector store saved to {vs_path}")

if __name__ == "__main__":
    create_vec_education()


