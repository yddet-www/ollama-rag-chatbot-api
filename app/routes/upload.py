# Author: Atishay Jain

# app/routes/upload.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
import os

DOCUMENTS_DIR = "documents"
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

router = APIRouter()

# Upload endpoint for supported document formats
@router.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        if not file.filename.endswith((".txt", ".xml", ".docx", ".csv", ".pdf", ".pptx")):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Allowed: .txt, .xml, .docx, .csv, .pdf, .pptx"
            )

        filepath = os.path.join(DOCUMENTS_DIR, file.filename)
        contents = await file.read()
        with open(filepath, "wb") as f:
            f.write(contents)

    return {"message": f"Successfully uploaded {len(files)} file(s)."}



