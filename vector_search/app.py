from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .embeddings import get_embedder
from .store import VectorIndex

app = FastAPI(title='Vector Search')

embedder = None
index = VectorIndex(metric='cosine')

class IndexRequest(BaseModel):
    texts: List[str]
    metadatas: Optional[List[dict]] = None

class SearchRequest(BaseModel):
    query: str
    k: Optional[int] = 5

@app.on_event('startup')
def startup_event():
    global embedder
    embedder = get_embedder()

@app.post('/index')
async def create_index(req: IndexRequest):
    try:
        vecs = embedder.embed(req.texts)
        index.fit(vecs, metadatas=req.metadatas)
        index.save('index.joblib')
        return {'status': 'ok', 'count': len(vecs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/search')
async def search(req: SearchRequest):
    try:
        qvec = embedder.embed([req.query])[0]
        results = index.query(qvec, k=req.k)
        return {'results': results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/health')
async def health():
    return {'status':'ok'}
