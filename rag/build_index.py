from dotenv import load_dotenv

from rag.chunker import chunk_text
from rag.embeddings import EmbeddingClient
from rag.loader import load_documents
from rag.vector_store import VectorStore

DOCUMENTS_DIR = "rag/documents"


def main() -> None:
    load_dotenv()

    documents = load_documents(DOCUMENTS_DIR)
    if not documents:
        print(f"No documents found in {DOCUMENTS_DIR}/")
        return

    chunks = []
    for doc in documents:
        for i, text in enumerate(chunk_text(doc["text"])):
            chunks.append({"source": doc["source"], "chunk_index": i, "text": text})

    embedder = EmbeddingClient()
    embeddings = embedder.embed([c["text"] for c in chunks])
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    store = VectorStore()
    store.build(chunks)

    print(f"Indexed {len(chunks)} chunks from {len(documents)} document(s).")


if __name__ == "__main__":
    main()
