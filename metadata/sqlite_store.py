from metadata_manager import MetadataManager
import sqlite3
import os
from typing import List, Tuple

class SQLiteStore(MetadataManager):
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)

    def initialize_store(self) -> bool:
        """Initialize the SQLite database and create the necessary table."""
        try:
            ## self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE,
                    file_hash TEXT,
                    source TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error initializing store: {e}")
            return False

    def upsert_file_metadata(self, file_path: str, file_hash: str, source: str) -> bool:
        """Upsert metadata for a given file."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO documents (file_path, file_hash, source)
                VALUES (?, ?, ?)
                ON CONFLICT(file_path) DO UPDATE SET
                    file_hash=excluded.file_hash,
                    source=excluded.source,
                    last_updated=CURRENT_TIMESTAMP
            """, (file_path, file_hash, source))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error upserting metadata: {e}")
            return False

    def delete_file_metadata(self, file_path: str) -> bool:
        """Delete metadata for a given file."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM documents WHERE file_path = ?", (file_path,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting metadata: {e}")
            return False

    def get_existing_files_status(self, files: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Get the status of files (new, modified) given a list of files and hashes"""
        status = []
        try:
            cursor = self.conn.cursor()
            for file_path, file_hash in files:
                cursor.execute("SELECT file_hash FROM documents WHERE file_path = ?", (file_path,))
                row = cursor.fetchone()
                if row is None:
                    status.append((file_path, "new"))
                elif row[0] != file_hash:
                    status.append((file_path, "modified"))
                else:
                    status.append((file_path, "unchanged"))
            return status
        except Exception as e:
            print(f"Error fetching existing files status: {e}")
            return []

    def get_missing_files(self, source: str, current_files: list) -> List[str]:
        """Get the list of files that have been deleted since the last run."""
        try:
            cursor = self.conn.cursor()
            placeholders = ','.join('?' for _ in current_files)
            cursor.execute("SELECT file_path FROM documents where source = ? AND file_path NOT IN ({})".format(placeholders), 
                           source, current_files)
            db_files = {row[0] for row in cursor.fetchall()}
            current_files_set = set(current_files)
            missing_files = list(db_files - current_files_set)
            return missing_files
        except Exception as e:
            print(f"Error fetching missing files: {e}")
            return []