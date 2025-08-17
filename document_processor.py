from langchain_core.documents import Document

class BaseDocumentProcessor:
    def process(self, uri: str) -> list[Document]:
        """Process a document and return the processed content."""
        raise NotImplementedError("This method should be overridden by subclasses.")