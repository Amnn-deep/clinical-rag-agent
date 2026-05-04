import io
import PyPDF2

class DocumentParser:
    @staticmethod
    def extract_and_chunk(file_bytes: bytes, chunk_size: int = 1000, overlap: int = 150) -> list:
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + " "
        
        clean_text = " ".join(full_text.split())
        if not clean_text: return []

        chunks = []
        for i in range(0, len(clean_text), chunk_size - overlap):
            chunk = clean_text[i : i + chunk_size]
            if len(chunk) > 50:
                chunks.append(chunk)
        return chunks