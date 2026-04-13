from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_PROVIDER = os.getenv('EMBEDDING_PROVIDER', 'local')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
VECTOR_STORE = os.getenv('VECTOR_STORE', 'sklearn')

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Simple guard: if using remote providers, ensure keys are present when required
if EMBEDDING_PROVIDER == 'gemini' and not GEMINI_API_KEY:
    raise RuntimeError('GEMINI_API_KEY not set but EMBEDDING_PROVIDER is gemini')
if EMBEDDING_PROVIDER == 'openai' and not OPENAI_API_KEY:
    raise RuntimeError('OPENAI_API_KEY not set but EMBEDDING_PROVIDER is openai')
