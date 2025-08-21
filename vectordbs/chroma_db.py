from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from vector_db import BaseVectorDB

class ChromaDB(BaseVectorDB):
    def __init__(self, persist_directory = "chroma_db", collection_name="data_store", 
                 embedding_model="sentence-transformers/all-mpnet-base-v2"):
        """Initialize the ChromaDB with the specified parameters."""
        super().__init__()

        embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.chroma_db = Chroma(persist_directory=persist_directory,
                    embedding_function=embeddings,
                    collection_name=collection_name)
        
    def upsert(self, docs: list[Document]):
        self.chroma_db.add_documents(docs)
