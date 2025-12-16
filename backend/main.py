from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import chromadb
from chromadb.utils import embedding_functions
import uuid

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create files directory if it doesn't exist
FILES_DIR = "file"
os.makedirs(FILES_DIR, exist_ok=True)

# Initialize ChromaDB
# 1. Setup persistent client
CHROMA_DB_DIR = "chroma_db"
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

# 2. Setup embedding function
# Using a lightweight, popular model: all-MiniLM-L6-v2
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 3. Get or create collection
collection = client.get_or_create_collection(
    name="documents",
    embedding_function=sentence_transformer_ef
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(FILES_DIR, file.filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Read the file content
    content = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        return {"filename": file.filename, "content": "File saved, but content is not valid UTF-8 text. vectorization skipped."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    if content:
        try:
            # Generate a unique ID for the document
            doc_id = str(uuid.uuid4())
            
            # Simple chunking can be added here if needed, but for now we embed the whole file content (if it's not too huge)
            # or we can split it. Let's do a simple add operation.
            collection.add(
                documents=[content],
                metadatas=[{"filename": file.filename}],
                ids=[doc_id]
            )
            return {
                "filename": file.filename, 
                "content": content, 
                "vector_db_status": "Successfully added to ChromaDB",
                "doc_id": doc_id
            }
        except Exception as e:
            print(f"Vector DB Error: {e}")
            return {
                "filename": file.filename, 
                "content": content, 
                "vector_db_status": f"Failed to add to Vector DB: {str(e)}"
            }
        
    return {"filename": file.filename, "content": content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
