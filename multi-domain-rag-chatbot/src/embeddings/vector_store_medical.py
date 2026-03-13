import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

RAW_PATH = "data/processed/medical/medical_clean.jsonl"
FAISS_PATH = "vectorstores/medical_faiss"

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_medical_docs(raw_path: str):
    print("→ Loading cleaned medical JSONL...")
    docs = []

    with Path(raw_path).open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            docs.append(Document(page_content=item["text"], metadata={"title": item.get("title", "")}))

    print(f"✔ Loaded {len(docs)} medical documents")
    return docs


def create_medical_vectorstore():
    jsonl_path = (PROJECT_ROOT / RAW_PATH).resolve()
    vs_path = (PROJECT_ROOT / FAISS_PATH).resolve()

    print("JSONL Path:", jsonl_path)
    print("Vectorstore Path:", vs_path)

    if not jsonl_path.exists():
        raise FileNotFoundError(f"Processed JSONL not found at {jsonl_path}")

    docs = load_medical_docs(jsonl_path)

    print("→ Chunking documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"✔ Created {len(chunks)} chunks")

    print("→ Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    print("✔ Embedding model loaded")

    print("→ Creating FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("✔ FAISS index created")

    print("→ Saving FAISS index...")
    vs_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(vs_path)
    print("🎉 FAISS vectorstore saved successfully!")


if __name__ == "__main__":
    create_medical_vectorstore()
