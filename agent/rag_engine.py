import os
import chromadb
from pathlib import Path
from chromadb.utils import embedding_functions

class AetherRAG:
    def __init__(self, vault_paths):
        # Convert single path to list for backward compatibility
        self.vault_paths = [Path(p) for p in (vault_paths if isinstance(vault_paths, list) else [vault_paths])]
        # Use the first path as the primary for DB storage
        self.db_path = self.vault_paths[0] / ".rag_db"
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Use a lightweight local embedding function
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name="aethervault",
            embedding_function=self.emb_fn
        )

    def index_vault(self):
        """Indexes all markdown files in all configured vault paths."""
        documents = []
        metadatas = []
        ids = []
        
        for vault_path in self.vault_paths:
            if not vault_path.exists(): continue
            for p in vault_path.glob("**/*.md"):
                if ".rag_db" in str(p): continue
                try:
                    content = p.read_text(encoding="utf-8")
                    if not content.strip(): continue
                    
                    documents.append(content)
                    metadatas.append({"filename": p.name, "path": str(p)})
                    ids.append(str(p))
                except Exception as e:
                    print(f"Error indexing {p}: {e}")
        
        if documents:
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        return len(documents)

    def query(self, text, n_results=5):
        """Finds the most relevant snippets for a query."""
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        
        context = ""
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                context += f"### Source: {meta['filename']}\n{doc}\n\n"
        return context
