from langchain_core.embeddings import Embeddings
import numpy as np
from sentence_transformers import SentenceTransformer
# Tạo wrapper class cho SentenceTransformer
from typing import Dict, Optional, List
class VietnameseEmbeddings(Embeddings):
    """Singleton Embeddings for Vietnamese using SentenceTransformer."""
    _instance: Optional['VietnameseEmbeddings'] = None

    def __new__(cls, model_name: str = "dangvantuan/vietnamese-embedding"): #"dangvantuan/vietnamese-embedding" or "keepitreal/vietnamese-sbert"
        # Nếu chưa có instance, tạo mới
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Khởi tạo model chỉ một lần
            cls._instance._initialize_model(model_name)
        return cls._instance

    def _initialize_model(self, model_name: str):
        try:
            print(f"Initializing Vietnamese embedding model: {model_name}")
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Error initializing embedding model: {e}")
            raise

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode(text, convert_to_numpy=True).tolist()
    def embed_text(self, text: str)-> np.ndarray:  #using in RAPTOR (np.ndarray)
        return self.model.encode(text, convert_to_numpy=True)
