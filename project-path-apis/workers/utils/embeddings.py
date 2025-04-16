# backend/retrieval/embeddings.py

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
# Load a pre-trained model (only once)
# 'all-MiniLM-L6-v2' is a popular general-purpose model, ~110MB in size
class EmbedingsModel(object):
    """Generate """
    def __init__(self):
        """s3 connection"""
        self._model_name = "all-MiniLM-L6-v2"
        self._model = MODEL
        

    def get_embedding(self,text: str) -> np.ndarray:
        """
        Returns the embedding (numpy array) for a single piece of text.
        """
        embedding = self._model.encode(text, convert_to_numpy=True)
        return embedding

    def batch_get_embeddings(self,texts: List[str]) -> np.ndarray:
        """
        Returns embeddings for a list of texts in a single batch call.
        
        :param texts: List of text strings
        :return: Numpy array of shape (len(texts), embedding_dim)
        """
        embeddings = self._model.encode(texts, convert_to_numpy=True) 
        return embeddings
