import typing
import numpy as np
from .config import EMBEDDING_PROVIDER, EMBEDDING_MODEL, GEMINI_API_KEY, OPENAI_API_KEY

class EmbeddingProvider:
    def embed(self, texts: typing.List[str]) -> typing.List[typing.List[float]]:
        raise NotImplementedError()


class LocalEmbedder(EmbeddingProvider):
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            raise RuntimeError('sentence-transformers is required for local embeddings') from e
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: typing.List[str]) -> typing.List[typing.List[float]]:
        if not texts:
            return []
        arr = self.model.encode(texts, convert_to_numpy=True)
        return arr.astype(float).tolist()


class GeminiEmbedder(EmbeddingProvider):
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        try:
            import google.generativeai as genai
        except Exception as e:
            raise RuntimeError('google-generativeai is required for gemini embeddings') from e
        if not GEMINI_API_KEY:
            raise RuntimeError('GEMINI_API_KEY is not set')
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = model_name
        self.genai = genai

    def embed(self, texts: typing.List[str]) -> typing.List[typing.List[float]]:
        if not texts:
            return []
        res = self.genai.embed_content(model=self.model, content=texts, task_type='classification')
        return [e for e in res['embedding']]


def get_embedder(provider: str = EMBEDDING_PROVIDER, model: str = EMBEDDING_MODEL) -> EmbeddingProvider:
    provider = provider.lower()
    if provider == 'local':
        return LocalEmbedder(model_name=model)
    if provider == 'gemini':
        return GeminiEmbedder(model_name=model)
    # fallback to local
    return LocalEmbedder(model_name=model)
