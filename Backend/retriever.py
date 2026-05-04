import os
import pickle
import numpy as np

class Retriever:
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        dot_product = np.dot(vec1, vec2)
        norm_a = np.linalg.norm(vec1)
        norm_b = np.linalg.norm(vec2)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))

    @staticmethod
    def find_best_match(query_vector: np.ndarray, pkl_path: str = "clinical_vectors.pkl"):
        with open(pkl_path, "rb") as f:
            document_data = pickle.load(f)
            
        best_score = -1.0
        best_chunk = ""
        
        for text_chunk, vector_list in document_data.items():
            doc_vector = np.array(vector_list, dtype=np.float32)
            score = Retriever.cosine_similarity(query_vector, doc_vector)
            if score > best_score:
                best_score = score
                best_chunk = text_chunk
                
        return best_chunk, best_score