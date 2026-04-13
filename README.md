Vector Search — production-ready, secure, enterprise-grade scaffold

Overview
--------
This repository provides a production-ready vector search service designed for prototyping and small-scale production. It supports local embeddings (via sentence-transformers) and local vector search (scikit-learn). The code is intentionally modular so you can swap in FAISS, Annoy, or managed vector databases (Pinecone, Milvus, Weaviate) for production-grade scalability.

Highlights
- Secure secret management via `.env` and `python-dotenv`.
- Pluggable embedding providers: `local`, `gemini`, `openai` (via env vars).
- Pluggable vector stores: `sklearn` (default), optional FAISS/Annoy/Pinecone.
- FastAPI service with `/index` and `/search` endpoints for programmatic integration.
- Dockerfile for container deployment and GitHub Actions CI for testing.

Quickstart
----------
1. Copy `.env.example` to `.env` and set any required keys.

```powershell
copy .env.example .env
# edit .env and set GEMINI_API_KEY or OPENAI_API_KEY if using remote providers
```

2. Create virtualenv and install deps:

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

3. Run the API locally:

```powershell
uvicorn vector_search.app:app --reload --port 8000
```

4. Index some texts (example using curl):

```bash
curl -X POST http://localhost:8000/index -H "Content-Type: application/json" -d '{"texts":["hello world","goodbye"]}'
```

5. Search:

```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -d '{"query":"hello","k":2}'
```

Security
--------
- Never commit `.env` or secret values. Use `.env.example` as a template.
- For CI / deployment, use GitHub Secrets or your cloud provider secret manager.
- For large-scale production, use a managed vector DB (Pinecone, Milvus) and secure keys in your orchestration platform.

Next Steps / Production Advice
-----------------------------
- Replace `sklearn` index with FAISS or HNSW-based index for large corpora.
- Add persistent storage (S3 / Azure Blob) for vectors & metadata snapshots.
- Add batching, throttling, request authentication (API keys / OAuth), and monitoring.
- Add automated deployment (GitHub Actions -> Kubernetes / Cloud Run / App Service).

If you want, I can now: (A) implement FAISS/Annoy integration, (B) add authentication and rate-limiting to the API, (C) push these changes to your GitHub repo. Reply with the letter(s) you want next.
