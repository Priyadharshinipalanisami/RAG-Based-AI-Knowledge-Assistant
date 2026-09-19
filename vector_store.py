import numpy as np
from .embeddings import embed_texts, embed_query

class VectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = np.empty((0, 384), dtype=np.float32)

    def clear(self):
        self.documents = []
        self.embeddings = np.empty((0, 384), dtype=np.float32)

    def add_documents(self, chunks, metadata):
        if not chunks:
            return

        vectors = embed_texts(chunks)

        for chunk in chunks:
            self.documents.append({
                "text": chunk,
                "metadata": metadata.copy()
            })

        self.embeddings = (
            vectors if len(self.embeddings) == 0
            else np.vstack((self.embeddings, vectors))
        )

    def search(self, query, top_k=5):
        if not self.documents:
            return []

        query_vector = embed_query(query)
        scores = self.embeddings @ query_vector
        indices = np.argsort(scores)[::-1][:top_k]

        return [
            {
                "text": self.documents[i]["text"],
                "metadata": self.documents[i]["metadata"],
                "score": float(scores[i])
            }
            for i in indices
        ]
