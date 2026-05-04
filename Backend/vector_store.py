import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class VectorStoreManager:
    # Model loads locally - No API required
    model = SentenceTransformer('all-MiniLM-L6-v2')

    @staticmethod
    def generate_embeddings(chunks: list):
        embeddings = VectorStoreManager.model.encode(chunks)
        document_vector_store = {chunk: emb.tolist() for chunk, emb in zip(chunks, embeddings)}
        
        with open("clinical_vectors.pkl", "wb") as f:
            pickle.dump(document_vector_store, f)
        return True