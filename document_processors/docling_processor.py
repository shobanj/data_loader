from document_processor import BaseDocumentProcessor

from pathlib import Path
from langchain_core.documents import Document
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from hash import compute_hash

class DoclingProcessor(BaseDocumentProcessor):

    def __init__(self, chunk_size=500, overlap=50) -> None:
        super().__init__()

        self.chunk_size = chunk_size
        self.overlap = overlap

    def process(self, uri: str, hash : str = "") -> list[Document]:
        """Process a document and return the processed content."""
        # Here you would implement the logic to process the document
        # For demonstration, we will just create a Document object with the content
        
        if hash == "":
            hash = compute_hash(uri)

        docling = DoclingLoader(file_path=str(Path.from_uri(uri)), chunker=HybridChunker())
        docs = docling.load_and_split()

        loader_docs = []
        chunk_no = 0

        for doc in docs:
            loader_doc = Document(
                page_content=doc.page_content,
                metadata={
                    "id": doc.metadata.get("source", "unknown_id"),
                    "source": uri,
                    "mimetype": doc.metadata["dl_meta"]["origin"]["mimetype"],
                    "chunk_no": chunk_no,
                    "hash": hash,
                }
            )
            chunk_no += 1
            loader_docs.append(loader_doc)

        return loader_docs