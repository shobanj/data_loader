registry = {
    "local_folder": "data_loaders.folder_source.FolderSource",
    "ftp": "data_loaders.ftp_source.FTPSource",
    "docling": "document_processors.docling_processor.DoclingProcessor",
    "litellm": "embedders.litellm_embedder.LiteLLMEmbedder",
    "huggingface": "embedders.huggingface_embedder.HuggingFaceEmbedder",
    "chroma": "vectordbs.chroma_db.ChromaDB",
    "qdrant": "vectordbs.qdrant_db.QdrantDB",
    "sqlite": "metadata.sqlite_store.SQLiteStore"
}