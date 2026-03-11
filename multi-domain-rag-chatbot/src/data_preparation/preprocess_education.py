import json
from pathlib import Path
from typing import Any

RAW_PATH = "data/raw/education/1.json"
OUT_PATH = "data/processed/education/processed_1.jsonl"

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def clean_text(s: Any) -> str:
    if s is None:
        return ""
    return " ".join(str(s).split())

def preprocess_education(raw_path: str = RAW_PATH, out_path: str = OUT_PATH):
    raw_path = Path(raw_path)
    if not raw_path.is_absolute():
        raw_path = (PROJECT_ROOT / raw_path).resolve()
    out_path = Path(out_path)
    if not out_path.is_absolute():
        out_path = (PROJECT_ROOT / out_path).resolve()

    print("cwd:", Path.cwd())
    print("project_root:", PROJECT_ROOT)
    print("using raw_path:", raw_path)
    print("using out_path:", out_path)

    if not raw_path.exists():
        parent = raw_path.parent
        print(f"Raw data file not found at {raw_path}")
        if parent.exists():
            print("Files in", parent, ":")
            for p in sorted(parent.iterdir()):
                print("  ", p.name)
        else:
            print(f"Folder {parent} does not exist")
        raise FileNotFoundError(f"Raw data file not found at {raw_path}")

    try:
        with raw_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON file {raw_path}: {e}") from e

    processed_data = []
    for article in data.get("data", []) if isinstance(data, dict) else (data if isinstance(data, list) else []):
        title = article.get("title", "")
        for para in article.get("paragraphs", []) or []:
            context = clean_text(para.get("context", ""))   
            if context:
                processed_data.append({"title": title, "context": context})

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for item in processed_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Wrote {len(processed_data)} records to {out_path}")

if __name__ == "__main__":
    preprocess_education()

