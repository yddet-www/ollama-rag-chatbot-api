# Author: Atishay Jain

# app/utils/settings.py

import tempfile
import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama


# Model configuration
OLLAMA_MODEL = "smollm"

# LLM and Embedding model initialization
embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
llm = ChatOllama(model=OLLAMA_MODEL)

# Directory setup
UPLOAD_DIR = tempfile.mkdtemp()
DOCUMENTS_DIR = "documents"
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# Text splitter configuration
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=500)

