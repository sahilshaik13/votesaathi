"""
RAG service — queries the Vertex AI RAG Engine for grounded answers.
"""

from google.genai import Client
from config import GCP_PROJECT_ID, GCP_PROJECT_NUMBER, GCP_LOCATION, RAG_CORPUS_ID, GEMINI_MODEL


def search_rag(query: str, top_k: int = 5) -> list[dict]:
    """
    Search the official Election Commission of India (ECI) rulebooks and documents.
    ALWAYS use this tool to find specific forms (like Form 6, Form 6A, etc.), 
    voter registration procedures, NRI voting rules, and official guidelines.
    
    Args:
        query: A detailed, self-contained search query. If the user asks a follow-up 
               (e.g., "what form do they need?"), rewrite the query to include context 
               (e.g., "What form do NRI voters need to register?").
        top_k: Number of results to return.

    Returns:
        List of dicts with keys: 'text', 'source_uri', 'score'.
    """
    if not RAG_CORPUS_ID:
        return []

    client = Client(vertexai=True, project=GCP_PROJECT_ID, location=GCP_LOCATION)
    # Perform a cross-region RAG lookup since our corpus is in Netherlands (europe-west4)
    corpus_name = f"projects/{GCP_PROJECT_NUMBER}/locations/europe-west4/ragCorpora/{RAG_CORPUS_ID}"

    response = client.models.generate_content(
        model=GEMINI_MODEL,
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
