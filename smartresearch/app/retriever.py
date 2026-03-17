"""
Retriever — embeds a user query and searches Endee for the most relevant chunks.

Endee SDK (v0.1.18) API notes:
  - filter must be a LIST of dicts: [{"field": {"$eq": value}}]
  - query() returns a list of dicts, NOT objects
"""
from typing import List, Dict, Any, Optional

from sentence_transformers import SentenceTransformer
from endee import Endee

from app.config import (
    ENDEE_BASE_URL,
    ENDEE_AUTH_TOKEN,
    ENDEE_INDEX_NAME,
    EMBEDDING_MODEL,
    TOP_K_RESULTS,
)


def get_endee_client() -> Endee:
    token = ENDEE_AUTH_TOKEN if ENDEE_AUTH_TOKEN else None
    client = Endee(token) if token else Endee()
    client.set_base_url(ENDEE_BASE_URL)
    return client


def retrieve(
    query: str,
    top_k: int = TOP_K_RESULTS,
    model: Optional[SentenceTransformer] = None,
    source_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Embed a query and return the top-K most similar chunks from Endee.

    Args:
        query:         Natural language question or search phrase.
        top_k:         Number of results to return.
        model:         Pre-loaded SentenceTransformer (loaded on demand if None).
        source_filter: Optional source filename to restrict search scope.

    Returns:
        List of dicts with keys: id, similarity, text, source, page, chunk_index
    """
    # Embed the query
    if model is None:
        model = SentenceTransformer(EMBEDDING_MODEL)
    query_vector = model.encode([query], normalize_embeddings=True)[0].tolist()

    # Endee filter MUST be a list of dicts — e.g. [{"source": {"$eq": "file.pdf"}}]
    filters = None
    if source_filter:
        filters = [{"source": {"$eq": source_filter}}]

    # Query Endee
    client = get_endee_client()
    
    # Check if index exists first to avoid "Required files missing" on empty DBs
    indexes = client.list_indexes()
    if isinstance(indexes, dict) and "indexes" in indexes:
        indexes = indexes["indexes"]
        
    existing = []
    for idx in (indexes or []):
        name = ""
        if isinstance(idx, str):
            name = idx
        elif isinstance(idx, dict):
            name = idx.get("index_name") or idx.get("name") or ""
        else:
            # For objects (and mocks), try index_name then name, but only if they are strings
            iname = getattr(idx, "index_name", None)
            if isinstance(iname, str):
                name = iname
            else:
                iname = getattr(idx, "name", None)
                if isinstance(iname, str):
                    name = iname
        
        if name:
            existing.append(name)
            
    if ENDEE_INDEX_NAME not in existing:
        return []

    index = client.get_index(name=ENDEE_INDEX_NAME)

    # Endee query() returns a list of dicts (not objects)
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        filter=filters,
    )

    chunks = []
    for r in results:
        meta = {}
        item_id = ""
        similarity = 0.0
        
        # Handle if r is an object (VectorItem)
        if hasattr(r, "meta"):
            meta = r.meta or {}
            item_id = getattr(r, "id", "")
            similarity = getattr(r, "similarity", 0.0)
        # Handle if r is a dict
        elif isinstance(r, dict):
            meta = r.get("meta") or {}
            item_id = r.get("id", "")
            similarity = r.get("similarity", 0.0)
            
        chunks.append({
            "id": item_id,
            "similarity": round(float(similarity), 4),
            "text": meta.get("text", "") if isinstance(meta, dict) else getattr(meta, "text", ""),
            "source": meta.get("source", "unknown") if isinstance(meta, dict) else getattr(meta, "source", "unknown"),
            "page": meta.get("page", 0) if isinstance(meta, dict) else getattr(meta, "page", 0),
            "chunk_index": meta.get("chunk_index", 0) if isinstance(meta, dict) else getattr(meta, "chunk_index", 0),
        })

    return chunks
