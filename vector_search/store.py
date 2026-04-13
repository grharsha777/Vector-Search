import os
import joblib
import numpy as np
from sklearn.neighbors import NearestNeighbors
from typing import List, Any, Dict

class VectorIndex:
    def __init__(self, metric: str = 'cosine'):
        self.metric = metric
        self._nn = None
        self.vectors = None
        self.metadatas = []

    def fit(self, vectors: List[List[float]], metadatas: List[Dict[str, Any]] = None):
        if vectors is None or len(vectors) == 0:
            raise ValueError('No vectors to index')
        self.vectors = np.array(vectors, dtype=float)
        self.metadatas = metadatas or [{} for _ in range(len(vectors))]
        self._nn = NearestNeighbors(n_neighbors=min(10, len(self.vectors)), metric=self.metric, n_jobs=-1)
        self._nn.fit(self.vectors)

    def query(self, qvec: List[float], k: int = 5):
        if self._nn is None:
            raise RuntimeError('Index not fitted')
        dists, idxs = self._nn.kneighbors(np.array(qvec, dtype=float).reshape(1, -1), n_neighbors=min(k, len(self.vectors)))
        results = []
        for dist, idx in zip(dists[0], idxs[0]):
            results.append({'score': float(dist), 'metadata': self.metadatas[int(idx)], 'index': int(idx)})
        return results

    def save(self, path: str = 'index.joblib'):
        joblib.dump({'vectors': self.vectors, 'metadatas': self.metadatas, 'metric': self.metric}, path)

    def load(self, path: str = 'index.joblib'):
        data = joblib.load(path)
        self.vectors = np.array(data['vectors'], dtype=float)
        self.metadatas = data.get('metadatas', [{} for _ in range(len(self.vectors))])
        self.metric = data.get('metric', self.metric)
        self._nn = NearestNeighbors(n_neighbors=min(10, len(self.vectors)), metric=self.metric, n_jobs=-1)
        self._nn.fit(self.vectors)
