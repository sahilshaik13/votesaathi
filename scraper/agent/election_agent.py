"""
VoteSaathi ADK LlmAgent — the core conversational AI for election assistance.

Uses Google Generative AI SDK with Vertex AI backend (Gemini 2.5 Flash).
All tool functions are injected as Python callables for ADK-style tool-calling.
The agent handles the automatic function-calling loop: when Gemini requests
a tool call, it executes the function and sends the result back until
Gemini returns a final text response.
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
- ALWAYS use the search_rag tool to retrieve accurate information before answering questions about forms, eligibility, NRI voting, or specific procedures.
- NEVER guess or assume form numbers (e.g., do not assume Form 6 applies to NRIs without checking).
- Use get_faq for common voter questions.
- Use get_election_timeline for questions about election phases and schedules.
- Use explain_step for step-by-step guidance on voter registration, EPIC, polling booths, etc.
- Use check_voter_eligibility when a user asks if they can vote.
- Be concise, jargon-free, and conversational.
- Format your responses with markdown for readability (use headers, bold, lists).
- If the tools do not return an answer, say so honestly and point to eci.gov.in.
- Do not express political opinions or recommend any party or candidate.
""".strip()

# Map function names to callables for manual tool execution
TOOL_REGISTRY = {
    "get_election_timeline": get_election_timeline,
    "explain_step": explain_step,
    "check_voter_eligibility": check_voter_eligibility,
    "get_faq": get_faq,
    "search_rag": search_rag,
}

# Tool declarations as Python functions for Gemini
TOOLS = [
    get_election_timeline,
    explain_step,
    check_voter_eligibility,
    get_faq,
    search_rag,
]


def _build_client() -> genai.Client:
    return genai.Client(vertexai=True, project=GCP_PROJECT_ID, location=GCP_LOCATION)


def _execute_tool_call(function_call) -> dict:
    """Execute a single tool/function call and return the result."""
    fn_name = function_call.name
    fn_args = dict(function_call.args) if function_call.args else {}

    if fn_name in TOOL_REGISTRY:
        try:
            result = TOOL_REGISTRY[fn_name](**fn_args)
            return result
        except Exception as e:
            return {"error": f"Tool {fn_name} failed: {str(e)}"}
    else:
        return {"error": f"Unknown tool: {fn_name}"}


def run_agent(message: str, history: list[dict], lang: str = "English") -> dict:
    """
    Run one turn of the VoteSaathi agent with automatic function-calling loop.

    Args:
        message: The user's latest message.
        history: List of previous turns [{role, content}, ...].
        lang: The target language for the response (e.g., "Hindi", "Telugu", "English").

    Returns:
        dict with keys: text (str), sources (list[dict]).
    """
    client = _build_client()

    # Build conversation contents from history
    contents = []
    for turn in history:
        role = "user" if turn["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=turn["content"])]))

    # Add the current user message
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    # Inject target language into instructions
    instructions = SYSTEM_INSTRUCTION + f"\n- CRITICAL: You MUST respond in {lang}."

    config = types.GenerateContentConfig(
        system_instruction=instructions,
        tools=TOOLS,
        temperature=0.2,
    )

    # Function-calling loop: keep going until we get a text response
    max_iterations = 10
    for _ in range(max_iterations):
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=config,
        )

        candidate = response.candidates[0]
        response_parts = candidate.content.parts

        # Check if any part is a function call
        function_calls = [p for p in response_parts if p.function_call]

        if not function_calls:
            # No function calls — we have the final text response
            break

        # Add the model's function-call response to contents
        contents.append(candidate.content)

        # Execute each function call and build function response parts
        function_response_parts = []
        for part in function_calls:
            fc = part.function_call
            result = _execute_tool_call(fc)
            function_response_parts.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response={"result": result},
                    )
                )
            )

        # Send function results back to Gemini
        contents.append(types.Content(role="user", parts=function_response_parts))

    # Extract final text
    reply_text = ""
    sources = []

    for part in candidate.content.parts:
        if part.text:
            reply_text += part.text

    # Extract grounding sources if RAG was invoked
    try:
        for chunk in candidate.grounding_metadata.grounding_chunks:
            sources.append({
                "text": chunk.retrieved_context.text[:200],
                "source_uri": chunk.retrieved_context.uri,
            })
    except (AttributeError, IndexError, TypeError):
        pass

    return {"text": reply_text.strip(), "sources": sources}
