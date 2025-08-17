from prefect import flow, task

import sqlite3
## from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
## from langchain_community.vectorstores import Chroma
import hashlib
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

def init_sqlite(db_path="hashes.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_hashes (
            id TEXT PRIMARY KEY,
            hash TEXT NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def has_changed(conn, doc_id, new_hash):
    cursor = conn.cursor()
    cursor.execute("SELECT hash FROM document_hashes WHERE id = ?", (doc_id,))
    row = cursor.fetchone()
    return row is None or row[0] != new_hash

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
conn = init_sqlite()
chroma_db = Chroma(persist_directory="./chroma_db",
                    embedding_function=embeddings,
                    collection_name="data_store")

## import chromadb
## from chromadb.config import Settings

def upsert_to_chroma(doc):
    chroma_db.add_documents([doc])
    ## chroma_db.add_embeddings([embedding_model.embed_query(content)], metadatas=[{"id": doc_id}], ids=[doc_id])
    ## chroma_db.add_texts([content], metadatas=[{"id": doc_id}], ids=[doc_id])

def update_sqlite(conn, doc_id, new_hash):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO document_hashes (id, hash)
        VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE SET hash = excluded.hash, last_updated = CURRENT_TIMESTAMP
    """, (doc_id, new_hash))
    conn.commit()

from pathlib import Path
import sqlite3
from prefect import task

@task
def sync_deleted_files(folder_path: str, db_path: str, vectorstore):
    # Step 1: Get current files
    current_files = set(str(p.resolve()) for p in Path(folder_path).glob("**/*") if p.is_file())

    # Step 2: Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path, vector_id FROM documents")
    db_files = cursor.fetchall()

    # Step 3: Find deleted files
    deleted = [(fp, vid) for fp, vid in db_files if fp not in current_files]

    # Step 4: Delete from vector DB and SQLite
    for file_path, vector_id in deleted:
        vectorstore.delete(ids=[vector_id])  # or use metadata filter
        cursor.execute("DELETE FROM documents WHERE file_path = ?", (file_path,))
        print(f"Deleted: {file_path}")

    conn.commit()
    conn.close()

@task
def load_documents():
    # Replace with your actual document loader
    doc = Document(page_content="Hello world", metadata={"id": "doc1"})
    return [doc]

@task
def process_document(doc):
    doc_id = doc.metadata.get("id", "unknown_id")
    content = doc.page_content
    new_hash = compute_hash(content)

    if has_changed(conn, doc_id, new_hash):
        upsert_to_chroma(doc)
        update_sqlite(conn, doc_id, new_hash)
        return f"Updated {doc_id}"
    else:
        return f"No change for {doc_id}"

@flow
def detect_changes_flow():
    
    docs = load_documents()
    results = [process_document(doc) for doc in docs]
    for r in results:
        print(r)

if __name__ == "__main__":
    detect_changes_flow()
