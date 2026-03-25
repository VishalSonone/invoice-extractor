from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.invoice import InvoiceData
from app.services.extractor import extract_invoice

router = APIRouter(prefix="/api")


@router.post("/upload", response_model=InvoiceData)
async def upload_invoice(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        result = extract_invoice(pdf_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    return result
