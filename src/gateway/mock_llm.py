"""Mock LLM Client.

Simulates a call to OpenAI/Anthropic. In production, this would use the
`openai` Python package. We use a mock to ensure the gateway is 100%
deterministic and testable without requiring API keys or paying for tokens.
"""

from __future__ import annotations


def generate_response(prompt: str, model: str) -> tuple[str, int]:
    """Returns a simulated LLM response and a fake token count."""
    
    # Simulate a model hallucinating a response based on the prompt
    if "[REDACTED" in prompt:
        reply = "I received your sanitized request. It looks like some data was redacted for security."
    else:
        reply = "This is a simulated LLM response to your clean prompt."
        
    # Fake token calculation (approx 1 token per 4 chars)
    fake_tokens_used = len(prompt) // 4 + len(reply) // 4
    
    return reply, fake_tokens_used
