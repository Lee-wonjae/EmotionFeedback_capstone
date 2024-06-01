from sentence_transformers import SentenceTransformer
import numpy as np

class text_embedding():
  def __init__(self, model_name):
    self.model_name = model_name

  def fit(self, X, y=None):
        return self
  
  def transform(self, X):
        embedding_model = SentenceTransformer(self.model_name)
        embedding_vec = embedding_model.encode(X['text'])
        X_val = np.concatenate((X.drop(['text'], axis = 1), embedding_vec), axis = 1)
        return X_val