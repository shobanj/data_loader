from document_processor import BaseDocumentProcessor

from pathlib import Path
from langchain_core.documents import Document
from langchain_docling import DoclingLoader

class DoclingProcessor(BaseDocumentProcessor):

    def __init__(self, chunk_size=500, overlap=50) -> None:
        super().__init__()

    def process(self, uri: str) -> list[Document]:
        """Process a document and return the processed content."""
        # Here you would implement the logic to process the document
        # For demonstration, we will just create a Document object with the content
        
        docling = DoclingLoader(file_path=Path.from_uri(uri))
        docs = docling.load_and_split()

        return docs