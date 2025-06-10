# Author: Atishay Jain

# app/routes/ask.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.settings import llm
from app.routes.process import vector_store
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

router = APIRouter()

# Request model for incoming questions
class QuestionRequest(BaseModel):
    question: str

# Format document chunks for context injection
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Endpoint to answer user questions using RAG
@router.post("/ask")
async def ask_question(request: QuestionRequest):
    if not vector_store:
        raise HTTPException(status_code=400, detail="Process documents first.")

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
