
# Author: Atishay Jain

# app/utils/loader.py
import os
from bs4 import BeautifulSoup
import docx
import PyPDF2
from pptx import Presentation
from langchain_core.documents import Document

# Load and parse various supported document formats
def load_documents(directory: str):
    documents = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                documents.append(Document(page_content=text, metadata={"source": filepath}))

            elif filename.endswith(".xml"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                soup = BeautifulSoup(content, "lxml-xml")
                text = soup.get_text(separator=" ", strip=True)
                documents.append(Document(page_content=text, metadata={"source": filepath}))

            elif filename.endswith(".docx"):
                doc = docx.Document(filepath)
                text = "\n".join([p.text for p in doc.paragraphs])
                documents.append(Document(page_content=text, metadata={"source": filepath}))

            elif filename.endswith(".pdf"):
                with open(filepath, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
                documents.append(Document(page_content=text, metadata={"source": filepath}))

            elif filename.endswith(".pptx"):
                prs = Presentation(filepath)
                texts = []
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if hasattr(shape, "text"):
                            texts.append(shape.text)
                text = "\n".join(texts)
                documents.append(Document(page_content=text, metadata={"source": filepath}))

            elif filename.endswith(".csv"):
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                documents.append(Document(page_content=text, metadata={"source": filepath}))

        except Exception as e:
            print(f"Error loading {filename}: {e}")
    return documents