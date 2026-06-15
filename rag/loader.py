import os
from typing import Dict, List

SUPPORTED_EXTENSIONS = (".md", ".txt")


def load_documents(directory: str) -> List[Dict]:
    documents = []
    if not os.path.exists(directory):
        return documents

    for filename in sorted(os.listdir(directory)):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue
        path = os.path.join(directory, filename)
        with open(path, "r", encoding="utf-8") as f:
            documents.append({"source": filename, "text": f.read()})

    return documents
