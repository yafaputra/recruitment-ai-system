import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "/content/drive/MyDrive/FinalProject_MultiAgentAI/vectorstore/chroma_db"
COLLECTION_NAME = "hr_policy_knowledge_base"

_embedding_model = None
_collection = None


def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(name=COLLECTION_NAME)
    return _collection


def retrieve(query: str, top_k: int = 3):
    embedding_model = _get_embedding_model()
    collection = _get_collection()
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results
