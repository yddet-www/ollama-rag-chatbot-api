from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.settings import llm, embeddings
from app.utils.vectorstore_state import vector_store, VECTOR_STORE_DIR
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    global vector_store

    # Always check if the vectorstore folder exists
    if not os.path.isdir(VECTOR_STORE_DIR):
        vector_store = None  # Invalidate in-memory reference
        raise HTTPException(status_code=400, detail="Documents not processed yet or deleted. Please call /process again.")

    # if vector_store is None:
    vector_store = FAISS.load_local(VECTOR_STORE_DIR, embeddings, allow_dangerous_deserialization=True)

    # Use MMR-based retriever for better semantic coverage
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 15}
    )

    # Improved prompt that encourages referencing source filenames
    prompt_template = """You are an assistant with access to the following documents.

Use only the context provided below to answer the question. If any of the source files seem relevant, mention them.

Context:
{context}

Question: {question}

Answer:
"""

    prompt = ChatPromptTemplate.from_template(prompt_template)

    rag_chain = (
        {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(request.question)
    return {"answer": answer}
