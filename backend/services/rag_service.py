"""
RAG service — queries the Vertex AI RAG Engine for grounded answers.
"""

from google.genai import Client
from config import GCP_PROJECT_ID, GCP_LOCATION, RAG_CORPUS_ID


def search_rag(query: str, top_k: int = 5) -> list[dict]:
    """
    Query Vertex AI RAG Engine and return top-k document chunks.

    Returns:
        List of dicts with keys: 'text', 'source_uri', 'score'.
    """
    if not RAG_CORPUS_ID:
        return []

    client = Client(vertexai=True, project=GCP_PROJECT_ID, location=GCP_LOCATION)
    corpus_name = f"projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION}/ragCorpora/{RAG_CORPUS_ID}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config={
            "tools": [{"retrieval": {"vertex_rag_store": {"rag_corpora": [corpus_name], "similarity_top_k": top_k}}}]
        },
    )

    chunks = []
    try:
        for grounding_chunk in response.candidates[0].grounding_metadata.grounding_chunks:
            chunks.append({
                "text": grounding_chunk.retrieved_context.text,
                "source_uri": grounding_chunk.retrieved_context.uri,
                "score": 1.0,
            })
    except (AttributeError, IndexError):
        pass

    return chunks
