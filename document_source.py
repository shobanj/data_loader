
class BaseDocumentSource:
    def get_documents_names(self) -> list[str]:
        """Retrieve the URI of documents from the source."""
        raise NotImplementedError("Subclasses should implement this method")
    
    def retrieve_document(self, doc: str) -> str:
        """Retrive a document from the source."""
        raise NotImplementedError("Subclasses should implement this method")
