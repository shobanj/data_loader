## Purpose of this class is to serve as an interface to manage metadata of all the artifacts 
## that are to be indexed in the vector database. This class lists the methods that we can 
## implement that allows to initialize the data store, maintain the list of files that are 
## indexed, their hashes, last updated data, file name etc., so that when we run the next time, 
## we can compute the differentials.

from typing import List, Tuple

class MetadataManager:
    def initialize_store(self) -> bool:
        """Initialize the metadata store if it does not exist."""
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def upsert_file_metadata(self, file_path: str, file_hash: str, source: str) -> bool:
        """Upsert metadata for a given file."""
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def delete_file_metadata(self, file_path: str) -> bool:
        """Delete metadata for a given file."""
        raise NotImplementedError("This method should be overridden by subclasses")

    def delete_files_metadata(self, file_paths: list) -> bool:
        """Delete metadata for a list of files."""
        for file in file_paths:
            self.delete_file_metadata(file)

        return True

    def get_existing_files_status(self, files: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Get the status of files (new, modified, unchanged)."""
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def get_missing_files(self, source: str, current_files: list) -> List[str]:
        """Get the list of files that have been deleted since the last run."""
        raise NotImplementedError("This method should be overridden by subclasses")