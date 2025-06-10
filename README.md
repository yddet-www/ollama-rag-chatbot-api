# RAG API with FastAPI + Ollama

This project is a document-based Retrieval-Augmented Generation (RAG) system using **FastAPI** and **Ollama**. It allows uploading multiple document types, creating vector embeddings, and asking questions based on document content using a local LLM model.

---

## Features

- Upload documents: `.txt`, `.docx`, `.pdf`, `.pptx`, `.xml`, `.csv`
- Extract and chunk document content
- Embed using local Ollama models (`llama3.2`)
- Ask questions with context-aware answers

---

## Requirements

- Python 3.10 or 3.11
- [Ollama](https://ollama.com) installed and running
- One of the supported Ollama models pulled (e.g. `llama3.2`)

---

## Installation

### 1. Clone the repository

```bash
git clone repo
cd repo
```

### 2. Set up virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Pull the Ollama Model

Make sure you have [Ollama installed](https://ollama.com/download). Then pull the required model:

```bash
ollama pull llama3.2
```

You can also use other models like `mistral`, `gemma`, or `llama2`.

> Update `OLLAMA_MODEL` in `app.py` if you change the model name.

---

## Run the App

```bash
python app.py
```

Or, if using Uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8001
```

---

## API Endpoints

### 1. Upload Documents

```http
POST /upload
```

**Form Data**: Upload one or more files (`.txt`, `.pdf`, `.docx`, `.pptx`, `.xml`, `.csv`)

---

### 2. Process Documents

```http
POST /process
```

Parses and embeds uploaded documents using Ollama.

---

### 3. Ask a Question

```http
POST /ask
```

**JSON Body**:

```json
{
  "question": "What is this document about?"
}
```

Returns a concise answer based on document context.

---

## Testing

You can test endpoints using:

- [Postman](https://www.postman.com/)
- [curl](https://curl.se/)
- Swagger UI: Visit `http://localhost:8001/docs`

---

## `requirements.txt`

```txt
fastapi
uvicorn
python-dotenv
beautifulsoup4
python-docx
PyPDF2
python-pptx
pydantic
langchain
langchain_ollama
faiss-cpu
```

---

## Notes

- Documents are stored in the `documents/` directory
- You must process the documents **before** asking questions
- Ollama must be running and the model must be pulled locally

---

