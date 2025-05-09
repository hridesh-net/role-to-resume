from io import BytesIO
from pdfminer.high_level import extract_text as extract_pdf
from docx import Document

def extract_resume_text(file_content: bytes, filename: str) -> str:
    if filename.endswith(".pdf"):
        return extract_pdf(BytesIO(file_content))
    elif filename.endswith(".docx"):
        return extract_docx(BytesIO(file_content))
    else:
        return file_content.decode("utf-8", errors="ignore")  # fallback to .txt

def extract_docx(file: BytesIO) -> str:
    document = Document(file)
    return "\n".join([para.text for para in document.paragraphs])