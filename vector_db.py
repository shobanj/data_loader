from langchain_chroma import Chroma
from langchain_core.documents import Document

class BaseVectorDB:
    def upsert(self, docs : list[Document]):
        raise NotImplementedError("This method should be overridden by subclasses.")
