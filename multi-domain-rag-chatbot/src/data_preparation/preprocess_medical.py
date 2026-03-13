import json
from pathlib import Path

RAW_PATH = "data/raw/medical/mediqa_raw.jsonl"
OUT_PATH = "data/processed/medical/medical_clean.jsonl"

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def clean_text(s):
    if not s:
        return ""
    return " ".join(str(s).split())


def preprocess_medical(raw_path: str = RAW_PATH, out_path: str = OUT_PATH):
    raw_path = Path(raw_path)
    if not raw_path.is_absolute():
        raw_path = (PROJECT_ROOT / raw_path).resolve()
    out_path = Path(out_path)
    if not out_path.is_absolute():
        out_path = (PROJECT_ROOT / out_path).resolve()

    print("Reading from:", raw_path)
    print("Saving to:", out_path)

    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data file not found at {raw_path}")

    processed = []

    with raw_path.open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)

            question = clean_text(item.get("instruction", ""))
            context = clean_text(item.get("input", ""))
            answer = clean_text(item.get("output", ""))

            # Combine question + context + answer into a single searchable text
            text = f"Question: {question} Context: {context} Answer: {answer}".strip()

            processed.append({
                "title": item.get("id", ""),
                "text": text
            })

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        for obj in processed:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print(f"Saved {len(processed)} processed medical records to {out_path}")


if __name__ == "__main__":
    preprocess_medical()
