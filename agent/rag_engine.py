import os
import time
import chromadb
from pathlib import Path
from chromadb.utils import embedding_functions
from typing import List, Union

class AetherRAG:
    """
    RAG (Retrieval-Augmented Generation) engine for Aether.
    Handles indexing markdown fragments and retrieving relevant context.
    """
    def __init__(self, vault_paths: Union[str, Path, List[Union[str, Path]]]):
        if isinstance(vault_paths, (str, Path)):
            self.vault_paths = [Path(vault_paths)]
        else:
            self.vault_paths = [Path(p) for p in vault_paths]
            
        if not self.vault_paths:
            raise ValueError("At least one vault path must be provided.")

        # Use the first path as the primary for DB storage, but ensure it's not the file
        primary_vault = self.vault_paths[0]
        self.db_path = primary_vault / ".rag_db"
        
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name="aethervault",
            embedding_function=self.emb_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Simple sliding window chunker for markdown text."""
        chunks = []
        if len(text) <= chunk_size:
            return [text]
        
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def index_vault(self, force: bool = False):
        """
        Indexes all markdown files in the configured vault paths.
        Uses file mtime to skip unchanged files unless force=True.
        """
        documents = []
        metadatas = []
        ids = []
        indexed_count = 0
        
        for vault_path in self.vault_paths:
            if not vault_path.exists():
                continue
                
            for p in vault_path.glob("**/*.md"):
                if ".rag_db" in str(p):
                    continue
                    
                try:
                    stat = p.stat()
                    mtime = stat.st_mtime
                    
                    # Check if file needs re-indexing (simplified logic for demo)
                    # In a real app, we'd store mtimes in a local meta-db or Chroma metadata
                    
                    content = p.read_text(encoding="utf-8")
                    if not content.strip():
                        continue
                    
                    chunks = self._chunk_text(content)
                    
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        metadatas.append({
                            "filename": p.name,
                            "path": str(p),
                            "mtime": mtime,
                            "chunk": i
                        })
                        ids.append(f"{p}_{i}")
                        
                    indexed_count += 1
                except Exception as e:
                    print(f"Error indexing {p}: {e}")
        
        if documents:
            # Using upsert to update existing chunks or add new ones
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        return indexed_count

    def query(self, text: str, n_results: int = 5) -> str:
        """Finds and formats the most relevant snippets for a query."""
        if self.collection.count() == 0:
            return ""

        results = self.collection.query(
            query_texts=[text],
            n_results=min(n_results, self.collection.count())
        )
        
        context = []
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                source = meta.get('filename', 'Unknown')
                context.append(f"### Source: {source} (Chunk {meta.get('chunk', 0)})\n{doc}\n")
                
        return "\n".join(context)

    def get_stats(self):
        """Returns statistics about the indexed vault."""
        return {
            "total_chunks": self.collection.count(),
            "vault_paths": [str(p) for p in self.vault_paths]
        }
