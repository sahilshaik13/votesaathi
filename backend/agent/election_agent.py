"""
VoteSaathi ADK LlmAgent — the core conversational AI for election assistance.

Uses Google Generative AI SDK with Vertex AI backend (Gemini 2.5 Flash).
All tool functions are injected as Python callables for ADK-style tool-calling.
"""

import json
from google import genai
from google.genai import types
from config import GCP_PROJECT_ID, GCP_LOCATION, GEMINI_MODEL
from agent.tools.get_timeline import get_election_timeline
from agent.tools.explain_step import explain_step
from agent.tools.check_eligibility import check_voter_eligibility
from agent.tools.get_faq import get_faq
from services.rag_service import search_rag

SYSTEM_INSTRUCTION = """
You are VoteSaathi, a helpful, accurate, and friendly AI assistant that helps Indian citizens 
understand the Indian election process. You serve first-time voters, students, researchers, 
and the general public.

Your knowledge is grounded in official Election Commission of India (ECI) documents.

Guidelines:
- Always use the available tools to retrieve accurate information before answering.
- Use search_rag for detailed questions about ECI rules, procedures, and documents.
- Use get_faq for common voter questions.
- Use get_election_timeline for questions about election phases and schedules.
- Use explain_step for step-by-step guidance on voter registration, EPIC, polling booths, etc.
- Use check_voter_eligibility when a user asks if they can vote.
- Be concise, jargon-free, and conversational.
- If you don't know the answer, say so honestly and point to eci.gov.in.
- Never make up facts about elections, laws, or candidates.
- Do not express political opinions or recommend any party or candidate.
""".strip()


def _build_client() -> genai.Client:
    return genai.Client(vertexai=True, project=GCP_PROJECT_ID, location=GCP_LOCATION)


def run_agent(message: str, history: list[dict]) -> dict:
    """
    Run one turn of the VoteSaathi agent.

    Args:
        message: The user's latest message.
        history: List of previous turns [{role, content}, ...].

    Returns:
        dict with keys: text (str), sources (list[dict]).
    """
    client = _build_client()

    # Build conversation contents
    contents = []
    for turn in history:
        role = "user" if turn["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=turn["content"])]))

    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    # Define tools as Python functions (ADK-style)
    tools = [
        get_election_timeline,
        explain_step,
        check_voter_eligibility,
        get_faq,
        search_rag,
    ]

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=tools,
            temperature=0.2,
        ),
    )

    reply_text = ""
    sources = []

    for candidate in response.candidates:
        for part in candidate.content.parts:
            if part.text:
                reply_text += part.text

    # Extract grounding sources if RAG was invoked
    try:
        for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
            sources.append({
                "text": chunk.retrieved_context.text[:200],
                "source_uri": chunk.retrieved_context.uri,
            })
    except (AttributeError, IndexError):
        pass

    return {"text": reply_text.strip(), "sources": sources}
