from sentence_transformers import SentenceTransformer
import numpy as np

class text_embedding():
    def __init__(self, model_name):
        self.model_name = model_name
        self.embedding_model = SentenceTransformer(self.model_name)

    def fit(self, X, y=None):
        return self
  
    def transform(self, texts):
        if isinstance(texts, list):
            embedding_vec = self.embedding_model.encode(texts)
        else:
            embedding_vec = self.embedding_model.encode(texts['text'].tolist())
        return embedding_vec
