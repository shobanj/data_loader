from document_source import BaseDocumentSource
from pathlib import Path

class FolderSource(BaseDocumentSource):
    def __init__(self, **kwargs):
        self.folder_path = kwargs["path"]
        self.glob = kwargs["filter"] if "glob" in kwargs.keys()  else "*"

    def get_documents_names(self) -> list[str]:
        """Retrieve the names of documents in the local folder."""
        return [str(file) for file in Path(self.folder_path).glob(self.glob) if file.is_file()]

    def retrieve_document(self, doc: str) -> str:
        """Retrieve a document from the local folder."""
        file_path = Path(doc).absolute()
        if not file_path.exists():
            raise FileNotFoundError(f"Document {doc} not found under {self.folder_path}")
        
        return file_path.as_uri()
