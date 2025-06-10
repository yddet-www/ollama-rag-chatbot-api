# Author: Atishay Jain

# app/routes/process.py
from fastapi import APIRouter, HTTPException
from app.utils.loader import load_documents
from app.utils.settings import text_splitter, embeddings, DOCUMENTS_DIR
from langchain_community.vectorstores import FAISS

router = APIRouter()

# Global vector store reference
vector_store = None

# Process and embed uploaded documents
@router.post("/process")
async def process_documents():
    global vector_store
    documents = load_documents(DOCUMENTS_DIR)

    if not documents:
        raise HTTPException(status_code=400, detail="No documents found to process.")

    split_docs = text_splitter.split_documents(documents)
    vector_store = FAISS.from_documents(split_docs, embeddings)
    return {"message": f"Processed {len(split_docs)} document chunks."}