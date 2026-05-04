from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, pickle, numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from parser import DocumentParser
from vector_store import VectorStoreManager
from retriever import Retriever
from llm_generator import LLMGenerator

load_dotenv(dotenv_path="../.env")

app = FastAPI()
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/upload-document/")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        chunks = DocumentParser.extract_and_chunk(file_bytes)
        if not chunks: raise HTTPException(status_code=400, detail="Empty PDF")
        VectorStoreManager.generate_embeddings(chunks)
        return {"status": "Success", "chunks": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask-clinical-agent/")
async def ask_clinical_agent(request: QueryRequest):
    try:
        if not os.path.exists("clinical_vectors.pkl"):
            raise HTTPException(status_code=400, detail="Upload PDF first")

        query_vector = embedding_model.encode([request.query])[0]
        best_chunk, score = Retriever.find_best_match(query_vector)
        
        # 0.40 is a safe threshold for MiniLM. Anything below this is likely unrelated.
        if score < 0.40:
            return {
                "answer": "The current clinical document does not contain any relevant information regarding your query.", 
                "retrieved_similarity": float(score)
            }
        
        answer = LLMGenerator.generate_response(best_chunk, request.query)
        return {"retrieved_similarity": float(score), "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)