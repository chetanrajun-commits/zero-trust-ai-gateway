"""FastAPI Application.

The web server that intercepts incoming LLM requests, runs them through
the Guardrails Engine, and forwards them to the LLM.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .guardrails import GuardrailsEngine
from .mock_llm import generate_response
from .models import ChatRequest, ChatResponse, SecurityReport

app = FastAPI(
    title="Zero-Trust AI Gateway",
    description="PII Redaction & Prompt Injection Defense for LLMs",
    version="0.1.0",
)

guardrails = GuardrailsEngine()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/chat/completions", response_model=ChatResponse)
def chat_completions(request: ChatRequest) -> ChatResponse:
    """Intercepts the chat request, enforces security, and calls the LLM."""
    
    # 1. Extract the user's latest prompt
    user_messages = [msg.content for msg in request.messages if msg.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user message provided.")
    
    raw_prompt = user_messages[-1]

    # 2. Check for Prompt Injection
    is_injection, injection_violations = guardrails.detect_injection(raw_prompt)
    if is_injection:
        return ChatResponse(
            reply="[BLOCKED] Prompt injection detected. Request denied.",
            security_report=SecurityReport(
                injection_blocked=True,
                violations=injection_violations
            )
        )

    # 3. Sanitize PII
    sanitized_prompt, pii_violations = guardrails.sanitize(raw_prompt)
    
    # 4. Call the LLM
    reply, tokens = generate_response(sanitized_prompt, request.model)
    
    # 5. Build the security report
    report = SecurityReport(
        pii_redacted=len(pii_violations) > 0,
        injection_blocked=False,
        violations=pii_violations
    )

    return ChatResponse(reply=reply, security_report=report)
