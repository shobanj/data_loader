from factory import load_config, get_component
from document_source import BaseDocumentSource
from document_processor import BaseDocumentProcessor
from vector_db import BaseVectorDB

from langchain_core.documents import Document

from hash import compute_hash

def main():
    config = load_config()

    loader : BaseDocumentSource = get_component(config["source"])
    local_files = [loader.retrieve_document(doc) for doc in loader.get_documents_names()]

    files_and_hashes = []
    for file in local_files:
        files_and_hashes.append((file, compute_hash(file)))

    processor : BaseDocumentProcessor = get_component(config["processor"])
    vector_db : BaseVectorDB = get_component(config["vector_db"])

    for file, hash in files_and_hashes:
        docs = processor.process(file, hash)
        for doc in docs:
            print(f"Processed document: {doc}...")

            vector_db.upsert(docs)

    """
    processor = get_component(config["processor"])
    embedder = get_component(config["embedder"])
    vector_db = get_component(config["vector_db"])
    sql_db = get_component(config["sql_db"])

    documents = source.get_documents()
    for doc in documents:
        chunks = processor.process(doc)
        embeddings = embedder.embed([chunk.content for chunk in chunks])
        vector_db.upsert(chunks, embeddings)
        sql_db.update_hash(doc.id, doc.hash)
    """

if __name__ == "__main__":
    main()