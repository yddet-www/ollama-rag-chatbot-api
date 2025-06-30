# app/routes/process.py
# Author - Atishay Jain 
from fastapi import APIRouter, HTTPException
from app.utils.loader import load_documents
from app.utils.settings import text_splitter, embeddings, DOCUMENTS_DIR
from app.utils.vectorstore_state import vector_store, VECTOR_STORE_DIR
from langchain_community.vectorstores import FAISS

router = APIRouter()

@router.post("/process")
async def process_documents():
    global vector_store
    documents = load_documents(DOCUMENTS_DIR)

    if not documents:
        raise HTTPException(status_code=400, detail="No documents found to process.")

    split_docs = text_splitter.split_documents(documents)
    vector_store = FAISS.from_documents(split_docs, embeddings)

    # Save the vector store to disk
    vector_store.save_local(VECTOR_STORE_DIR)

    return {"message": f"Processed and saved {len(split_docs)} document chunks."}
