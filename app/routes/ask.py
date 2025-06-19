# Author: Atishay Jain

# app/routes/ask.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.settings import llm, embeddings
from app.routes.process import vector_store, VECTOR_STORE_DIR
from langchain_community.vectorstores import FAISS  # Correct import
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os

router = APIRouter()

# Request model for incoming questions
class QuestionRequest(BaseModel):
    question: str

# Context injection - format documetn chunks
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    global vector_store

    # Try loading from disk if not already loaded
    if vector_store is None:
        if not os.path.isdir(VECTOR_STORE_DIR):
            raise HTTPException(status_code=400, detail="Documents not processed yet. Please call /process first.")
        vector_store = FAISS.load_local(VECTOR_STORE_DIR, embeddings, allow_dangerous_deserialization=True)

    retriever = vector_store.as_retriever(k=4)

    prompt_template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    Answer in a clear and concise manner. If you don't know the answer, say 'I don't know'."""

    prompt = ChatPromptTemplate.from_template(prompt_template)

    rag_chain = (
        {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(request.question)
    return {"answer": answer}
