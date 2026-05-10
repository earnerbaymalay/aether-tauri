import os
import chromadb
import argparse
from pathlib import Path
from chromadb.utils import embedding_functions

class AetherFS:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else Path.home() / ".aether" / "fs_db"
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name="aether_fs",
            embedding_function=self.emb_fn
        )

    def index_directory(self, target_dir, extensions=[".txt", ".py", ".sh", ".md", ".json"]):
        """Deep index a directory for semantic search."""
        target_path = Path(target_dir).expanduser()
        print(f"📂 Indexing: {target_path}")
        
        documents = []
        metadatas = []
        ids = []
        count = 0
        
        for p in target_path.glob("**/*"):
            if p.is_file() and p.suffix in extensions:
                if ".git" in str(p) or ".rag_db" in str(p) or "node_modules" in str(p):
                    continue
                    
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    if not content.strip(): continue
                    
                    # Chunk large files if needed (simplified here)
                    documents.append(content[:10000]) # Store first 10k chars
                    metadatas.append({"filename": p.name, "path": str(p)})
                    ids.append(str(p))
                    count += 1
                except Exception as e:
                    print(f"  [!] Error indexing {p.name}: {e}")
        
        if documents:
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        print(f"✅ Indexed {count} files.")
        return count

    def search(self, query, n_results=5):
        """Semantic search across indexed files."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

def main():
    parser = argparse.ArgumentParser(description="Aether Semantic File System")
    parser.add_argument("--index", help="Directory to index")
    parser.add_argument("--query", help="Search query")
    args = parser.parse_args()
    
    fs = AetherFS()
    
    if args.index:
        fs.index_directory(args.index)
    
    if args.query:
        results = fs.search(args.query)
        print("\n🔍 Search Results:")
        for i, doc in enumerate(results['documents'][0]):
            path = results['metadatas'][0][i]['path']
            print(f"\n--- {path} ---")
            print(doc[:200] + "...")

if __name__ == "__main__":
    main()
