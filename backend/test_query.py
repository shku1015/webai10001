import chromadb
from chromadb.utils import embedding_functions
import os

def test_query():
    # 1. Setup persistent client (must match the path used in main.py)
    # Assuming this script is run from backend/ directory
    CHROMA_DB_DIR = "chroma_db"
    
    if not os.path.exists(CHROMA_DB_DIR):
        print(f"Error: ChromaDB directory '{CHROMA_DB_DIR}' not found. Make sure you have uploaded files via the app first.")
        return

    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

    # 2. Setup embedding function (must match the model used in main.py)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    # 3. Get the collection
    try:
        collection = client.get_collection(
            name="documents",
            embedding_function=sentence_transformer_ef
        )
        print(f"Successfully loaded collection '{collection.name}' with {collection.count()} documents.")
    except Exception as e:
        print(f"Error loading collection: {e}")
        return

    # 4. Perform a query
    while True:
        query_text = input("\nEnter your query (or 'quit' to exit): ")
        if query_text.lower() == 'quit':
            break

        print(f"\nSearching for: '{query_text}'...")
        
        try:
            results = collection.query(
                query_texts=[query_text],
                n_results=3, # Returns top 3 matches
                include=['documents', 'metadatas', 'distances']
            )

            print("\n--- Results ---")
            if not results['ids'][0]:
                print("No matches found.")
            
            for i in range(len(results['ids'][0])):
                doc_id = results['ids'][0][i]
                distance = results['distances'][0][i]
                metadata = results['metadatas'][0][i]
                document = results['documents'][0][i]
                
                print(f"\nRank {i+1}:")
                print(f"ID: {doc_id}")
                print(f"Distance: {distance:.4f} (Lower is better)")
                print(f"Filename: {metadata.get('filename', 'Unknown')}")
                print(f"Content Preview: {document[:150]}...") # Show first 150 chars
                print("-" * 30)

        except Exception as e:
            print(f"Query Error: {e}")

if __name__ == "__main__":
    test_query()
