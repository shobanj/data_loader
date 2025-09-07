from factory import load_config, get_component
from document_source import BaseDocumentSource
from document_processor import BaseDocumentProcessor
from metadata_manager import MetadataManager
from vector_db import BaseVectorDB

from langchain_core.documents import Document

from hash import compute_hash

def main():
    config = load_config()

    loader : BaseDocumentSource = get_component(config["source"])
    
    metadata_db : MetadataManager = get_component(config["sql_db"])
    metadata_db.initialize_store()

    local_files = [loader.retrieve_document(doc) for doc in loader.get_documents_names()]

    files_and_hashes = []
    for file in local_files:
        files_and_hashes.append((file, compute_hash(file)))

    processor : BaseDocumentProcessor = get_component(config["processor"])
    vector_db : BaseVectorDB = get_component(config["vector_db"])
    sql_db = get_component(config["sql_db"])

    for file, hash in files_and_hashes:
        update_list = metadata_db.get_existing_files_status([(file, hash)])
        print(update_list)
        for _, stat in update_list:
            if stat in ("new", "modified"):
                print(f"New or modified file detected: {file}")

                docs = processor.process(file, hash)
                for doc in docs:
                    print(f"Processed document: {doc}...")

                    vector_db.upsert(docs)
                    metadata_db.upsert_file_metadata(file, hash, "folder_source")
            else:
                print(f"No changes in file: {file}")
                continue


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