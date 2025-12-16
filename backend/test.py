

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



try:
    # 컬렉션 생성 - 중복생성 시 오류
    collection = client.get_collection(name='documents')
except:
    collection = client.create_collection(name='documents')
# 있으면 가져오고, 없으면 생성해서 가져오고... 
collection = client.get_or_create_collection(name='documents')

results = collection.query(
    query_texts=[f"Resolving"],
    # query_embeddings=[get_sentence_embedding("This is a query document about 수학")], # Or you can embed it yourself
    n_results=2 # how many results to return
)

print(results)


collection.get()